from uuid import uuid4, UUID
from typing import List


from src.features.tournament.application.schemas import (
    ModalityCreate,
    TournamentCreate,
    CategoryCreate,
    CategoryRegistrationCreate,
    MassRegistrationRequest,
    CategoryBulkCreate,
    CategoryUpdate,
    RankGroupCreate,
    RankGroupUpdate,
)
from src.features.tournament.data.repository import (
    ModalityRepository,
    TournamentRepository,
    CategoryRepository,
    CategoryRegistrationRepository,
    RankGroupRepository,
)
from src.features.tournament.domain.entities import (
    Modality,
    Tournament,
    Category,
    CategoryModality,
    PhysicalRequirement,
    CategoryRegistration,
    RankGroup,
)
from src.features.tournament.data.models import (
    PhysicalRequirementModel,
    CategoryModalityModel,
    CategoryModel,
    RankGroupModel,
)
from src.features.registration.data.models import RankModel, SexModel
from src.features.registration.data.repository import (
    CompetitorRepository,
    RankRepository,
    SexRepository,
)
from src.features.registration.domain.entities import Competitor


class TournamentUseCases:
    def __init__(
        self,
        modality_repo: ModalityRepository,
        tournament_repo: TournamentRepository,
        category_repo: CategoryRepository,
        registration_repo: CategoryRegistrationRepository,
        competitor_repo: CompetitorRepository,
        rank_repo: RankRepository,
        sex_repo: SexRepository,
        rank_group_repo: RankGroupRepository,
    ):
        self.modality_repo = modality_repo
        self.tournament_repo = tournament_repo
        self.category_repo = category_repo
        self.registration_repo = registration_repo
        self.competitor_repo = competitor_repo
        self.rank_repo = rank_repo
        self.sex_repo = sex_repo
        self.rank_group_repo = rank_group_repo

    async def register_rank_group(self, schema: RankGroupCreate) -> RankGroup:
        ranks = []
        for rid in schema.rank_ids:
            rank = await self.rank_repo.get_by_id(rid)
            if not rank:
                raise ValueError(f"Rank with ID {rid} not found")
            ranks.append(rank)
        
        group = RankGroup(id=uuid4(), name=schema.name, ranks=ranks)
        return await self.rank_group_repo.create(group)

    async def list_rank_groups(self) -> List[RankGroup]:
        return await self.rank_group_repo.list_all()

    async def get_rank_group(self, id: UUID) -> RankGroup:
        group = await self.rank_group_repo.get_by_id(id)
        if not group:
            raise ValueError(f"Rank Group with ID {id} not found")
        return group

    async def update_rank_group(self, id: UUID, schema: RankGroupUpdate) -> RankGroup:
        model = await self.rank_group_repo.get_model_by_id(id)
        if not model:
            raise ValueError(f"Rank Group with ID {id} not found")
        
        if schema.name is not None:
            model.name = schema.name
        
        if schema.rank_ids is not None:
            model.ranks = []
            for rid in schema.rank_ids:
                r_model = await self.rank_repo.session.get(RankModel, rid)
                if r_model:
                    model.ranks.append(r_model)
        
        await self.rank_group_repo.session.flush()
        return await self.rank_group_repo.get_by_id(id)

    async def delete_rank_group(self, id: UUID) -> bool:
        return await self.rank_group_repo.delete(id)

    async def register_modality(self, schema: ModalityCreate) -> Modality:
        modality = Modality(id=uuid4(), name=schema.name)
        return await self.modality_repo.create(modality)

    async def list_modalities(self) -> List[Modality]:
        return await self.modality_repo.list_all()

    async def register_tournament(self, schema: TournamentCreate) -> Tournament:
        tournament = Tournament(id=uuid4(), description=schema.description)
        return await self.tournament_repo.create(tournament)

    async def list_tournaments(self) -> List[Tournament]:
        return await self.tournament_repo.list_all()

    async def register_category(self, schema: CategoryCreate) -> List[Category]:
        # 1. Fetch sexes
        sexes = []
        for sid in schema.sex_ids:
            sex = await self.sex_repo.get_by_id(sid)
            if not sex:
                raise ValueError(f"Sex with ID {sid} not found")
            sexes.append(sex)

        # 2. Create Domain Entity
        category_id = uuid4()
        category = Category(
            id=category_id,
            ages=schema.ages,
            special_condition=schema.special_condition,
            sexes=sexes,
        )

        # Cache for deduplicating physical requirements within the same request
        phys_req_cache: dict[tuple, PhysicalRequirement] = {}

        for mod_data in schema.modalities:
            modality = await self.modality_repo.get_by_id(mod_data.modality_id)
            if not modality:
                raise ValueError(f"Modality with ID {mod_data.modality_id} not found")

            # Collect physical requirement entities
            phys_req_entities = []
            for pr_schema in mod_data.physical_requirements:
                pr_key = (
                    pr_schema.initial_weight,
                    pr_schema.final_weight,
                    pr_schema.initial_height,
                    pr_schema.final_height,
                )
                if any(v is not None for v in pr_key):
                    if pr_key in phys_req_cache:
                        phys_req_entities.append(phys_req_cache[pr_key])
                    else:
                        new_pr = PhysicalRequirement(
                            id=uuid4(),
                            initial_weight=pr_schema.initial_weight,
                            final_weight=pr_schema.final_weight,
                            initial_height=pr_schema.initial_height,
                            final_height=pr_schema.final_height,
                        )
                        phys_req_cache[pr_key] = new_pr
                        phys_req_entities.append(new_pr)

            # If no physical requirements were provided (or all were empty),
            # we still need to create the category-modalities (one for each rank group)
            # but with physical_requirement=None.
            if not phys_req_entities:
                phys_req_entities = [None]

            for pr_entity in phys_req_entities:
                for rgid in mod_data.rank_group_ids:
                    rank_group = await self.rank_group_repo.get_by_id(rgid)
                    if not rank_group:
                        raise ValueError(f"Rank Group with ID {rgid} not found")

                    cat_mod = CategoryModality(
                        id=uuid4(),
                        category=category,
                        modality=modality,
                        rank_group=rank_group,
                        physical_requirement=pr_entity,
                    )
                    category.modalities.append(cat_mod)

        created = await self.category_repo.create(category)
        return [created]

    async def update_category(self, category_id: UUID, schema: CategoryUpdate) -> Category:
        model = await self.category_repo.get_model_by_id(category_id)
        if not model:
            raise ValueError(f"Category with ID {category_id} not found")

        # Update basic fields
        if schema.ages is not None:
            model.ages = schema.ages
        if schema.special_condition is not None:
            model.special_condition = schema.special_condition

        # Update sexes
        if schema.sex_ids is not None:
            model.sexes = []
            for sid in schema.sex_ids:
                sex_model = await self.sex_repo.session.get(SexModel, sid)
                if sex_model:
                    model.sexes.append(sex_model)

        # Update modalities
        if schema.modalities is not None:
            # Clear existing modalities (cascade delete-orphan handles the DB)
            model.modalities = []
            
            # Cache for deduplicating physical requirement models
            phys_req_model_cache: dict[tuple, PhysicalRequirementModel] = {}

            for mod_data in schema.modalities:
                modality = await self.modality_repo.get_by_id(mod_data.modality_id)
                if not modality:
                    raise ValueError(f"Modality with ID {mod_data.modality_id} not found")

                # Collect physical requirement models
                phys_req_models = []
                for pr_schema in mod_data.physical_requirements:
                    pr_key = (
                        pr_schema.initial_weight,
                        pr_schema.final_weight,
                        pr_schema.initial_height,
                        pr_schema.final_height,
                    )
                    if any(v is not None for v in pr_key):
                        if pr_key in phys_req_model_cache:
                            phys_req_models.append(phys_req_model_cache[pr_key])
                        else:
                            new_pr_model = PhysicalRequirementModel(
                                id=uuid4(),
                                initial_weight=pr_schema.initial_weight,
                                final_weight=pr_schema.final_weight,
                                initial_height=pr_schema.initial_height,
                                final_height=pr_schema.final_height,
                            )
                            self.category_repo.session.add(new_pr_model)
                            phys_req_model_cache[pr_key] = new_pr_model
                            phys_req_models.append(new_pr_model)

                # Case: no physical requirements
                if not phys_req_models:
                    phys_req_models = [None]

                for pr_model in phys_req_models:
                    # Create a CategoryModality record for EACH rank group ID
                    for rgid in mod_data.rank_group_ids:
                        rank_group = await self.rank_group_repo.get_by_id(rgid)
                        if not rank_group:
                            raise ValueError(f"Rank Group with ID {rgid} not found")

                        cat_mod_model = CategoryModalityModel(
                            id=uuid4(),
                            category_id=model.id,
                            modality_id=modality.id,
                            rank_group_id=rank_group.id,
                            physical_requirement_id=pr_model.id if pr_model else None,
                        )
                        model.modalities.append(cat_mod_model)

        # We don't need to call repository.create because the model is already in session and tracked
        # But we need to return the domain entity
        await self.category_repo.session.flush() # Ensure it's in DB
        return await self.category_repo.get_by_id(category_id)

    async def list_categories(self) -> List[Category]:
        return await self.category_repo.list_all()

    async def inscribe_competitor(self, schema: CategoryRegistrationCreate) -> CategoryRegistration:
        # 1. Fetch dependencies
        competitor = await self.competitor_repo.get_by_id(schema.competitor_id)
        if not competitor:
            raise ValueError(f"Competitor with ID {schema.competitor_id} not found")

        category_modality = await self.category_repo.get_modality_by_id(schema.category_modality_id)
        if not category_modality:
            raise ValueError(f"Category Modality with ID {schema.category_modality_id} not found")

        tournament = await self.tournament_repo.get_by_id(schema.tournament_id)
        if not tournament:
            raise ValueError(f"Tournament with ID {schema.tournament_id} not found")

        # 2. Create Domain Entity
        registration = CategoryRegistration(
            id=uuid4(),
            competitor=competitor,
            category_modality=category_modality,
            tournament=tournament,
        )

        return await self.registration_repo.create(registration)

    async def mass_register_competitors(
        self, schema: MassRegistrationRequest
    ) -> dict:
        # 1. Fetch tournament
        tournament = await self.tournament_repo.get_by_id(schema.tournament_id)
        if not tournament:
            raise ValueError(f"Tournament with ID {schema.tournament_id} not found")

        # 2. Fetch competitors by IDs
        competitors = await self.competitor_repo.get_by_ids(schema.competitor_ids)

        registrations: List[CategoryRegistration] = []
        errors: List[dict] = []

        if schema.category_modality_id:
            # 3a. Manual registration for a specific category-modality
            category_modality = await self.category_repo.get_modality_by_id(schema.category_modality_id)
            if not category_modality:
                raise ValueError(f"Category Modality with ID {schema.category_modality_id} not found")

            for competitor in competitors:
                failures = category_modality.get_eligibility_failures(competitor)
                if any(failures.values()):
                    errors.append({
                        "competitor_id": competitor.id,
                        "competitor_name": f"{competitor.first_name} {competitor.last_name}",
                        "message": "Competitor is not eligible for the selected category",
                        "reasons": failures,
                    })
                else:
                    registration = CategoryRegistration(
                        id=uuid4(),
                        competitor=competitor,
                        category_modality=category_modality,
                        tournament=tournament,
                    )
                    registrations.append(registration)
        else:
            # 3b. Automatic registration
            # Fetch all categories
            all_categories = await self.category_repo.list_all()
            
            # Flatten to all available CategoryModality options
            all_category_modalities: List[CategoryModality] = []
            for cat in all_categories:
                all_category_modalities.extend(cat.modalities)

            for competitor in competitors:
                # Find all eligible category-modalities
                eligible_mods = [m for m in all_category_modalities if m.is_eligible(competitor)]

                if not eligible_mods:
                    errors.append({
                        "competitor_id": competitor.id,
                        "competitor_name": f"{competitor.first_name} {competitor.last_name}",
                        "message": "No eligible category found for this competitor",
                        "reasons": None,
                    })
                    continue

                # Group unique matches by modality
                by_modality_name: dict[str, List[CategoryModality]] = {}
                for mod in eligible_mods:
                    name = mod.modality.name
                    if name not in by_modality_name:
                        by_modality_name[name] = []
                    by_modality_name[name].append(mod)

                for mod_name, mods in by_modality_name.items():
                    if len(mods) == 1:
                        # Exactly one eligible category-modality for this modality type
                        registration = CategoryRegistration(
                            id=uuid4(),
                            competitor=competitor,
                            category_modality=mods[0],
                            tournament=tournament,
                        )
                        registrations.append(registration)
                    else:
                        # Conflict: multiple eligible category-modalities for same modality type
                        errors.append({
                            "competitor_id": competitor.id,
                            "competitor_name": f"{competitor.first_name} {competitor.last_name}",
                            "message": f"Multiple categories found for modality '{mod_name}'. Impossible to choose automatically.",
                            "overlapping_categories": [m.category for m in mods], # Just for info
                            "reasons": None,
                        })

        # 4. Persist each registration
        for registration in registrations:
            await self.registration_repo.create(registration)

        return {"registrations": registrations, "errors": errors}

    async def get_competitors_by_category_modality(self, category_modality_id: UUID) -> List[Competitor]:
        registrations = await self.registration_repo.get_by_categories([category_modality_id])
        return [reg.competitor for reg in registrations]

    async def register_categories_bulk(self, schema: CategoryBulkCreate) -> List[Category]:
        all_created = []
        for category_schema in schema.categories:
            created = await self.register_category(category_schema)
            all_created.extend(created)
        return all_created
