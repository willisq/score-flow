from uuid import uuid4, UUID
from typing import List


from src.features.tournament.application.schemas import (
    ModalityCreate,
    TournamentCreate,
    CategoryCreate,
    CategoryRegistrationCreate,
    MassRegistrationRequest,
)
from src.features.tournament.data.repository import (
    ModalityRepository,
    TournamentRepository,
    CategoryRepository,
    CategoryRegistrationRepository,
)
from src.features.tournament.domain.entities import (
    Modality,
    Tournament,
    Category,
    CategoryRegistration,
)
from src.features.registration.data.repository import (
    CompetitorRepository,
    RankRepository,
    SexRepository,
)


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
    ):
        self.modality_repo = modality_repo
        self.tournament_repo = tournament_repo
        self.category_repo = category_repo
        self.registration_repo = registration_repo
        self.competitor_repo = competitor_repo
        self.rank_repo = rank_repo
        self.sex_repo = sex_repo

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

    async def register_category(self, schema: CategoryCreate) -> Category:
        # 1. Fetch dependencies
        modality = await self.modality_repo.get_by_id(schema.modality_id)
        if not modality:
            raise ValueError(f"Modality with ID {schema.modality_id} not found")

        ranks = []
        for rid in schema.rank_ids:
            rank = await self.rank_repo.get_by_id(rid)
            if not rank:
                raise ValueError(f"Rank with ID {rid} not found")
            ranks.append(rank)

        sexes = []
        for sid in schema.sex_ids:
            sex = await self.sex_repo.get_by_id(sid)
            if not sex:
                raise ValueError(f"Sex with ID {sid} not found")
            sexes.append(sex)

        # 2. Create Domain Entity
        category = Category(
            id=uuid4(),
            ages=schema.ages,
            special_condition=schema.special_condition,
            modality=modality,
            ranks=ranks,
            sexes=sexes,
            initial_weight=schema.initial_weight,
            final_weight=schema.final_weight,
            initial_height=schema.initial_height,
            final_height=schema.final_height,
        )

        return await self.category_repo.create(category)

    async def list_categories(self) -> List[Category]:
        return await self.category_repo.list_all()

    async def inscribe_competitor(self, schema: CategoryRegistrationCreate) -> CategoryRegistration:
        # 1. Fetch dependencies
        competitor = await self.competitor_repo.get_by_id(schema.competitor_id)
        if not competitor:
            raise ValueError(f"Competitor with ID {schema.competitor_id} not found")

        category = await self.category_repo.get_by_id(schema.category_id)
        if not category:
            raise ValueError(f"Category with ID {schema.category_id} not found")

        tournament = await self.tournament_repo.get_by_id(schema.tournament_id)
        if not tournament:
            raise ValueError(f"Tournament with ID {schema.tournament_id} not found")

        # 2. Create Domain Entity (Validation can be added here if needed, 
        # e.g., checking if competitor fits the category)
        registration = CategoryRegistration(
            id=uuid4(),
            competitor=competitor,
            category=category,
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

        if schema.category_id:
            # 3a. Manual registration for a specific category
            category = await self.category_repo.get_by_id(schema.category_id)
            if not category:
                raise ValueError(f"Category with ID {schema.category_id} not found")

            for competitor in competitors:
                failures = category.get_eligibility_failures(competitor)
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
                        category=category,
                        tournament=tournament,
                    )
                    registrations.append(registration)
        else:
            # 3b. Automatic registration (enhanced logic)
            # Fetch all categories
            categories = await self.category_repo.list_all()

            for competitor in competitors:
                # Find all eligible categories
                eligible_cats = [c for c in categories if c.is_eligible(competitor)]

                if not eligible_cats:
                    errors.append({
                        "competitor_id": competitor.id,
                        "competitor_name": f"{competitor.first_name} {competitor.last_name}",
                        "message": "No eligible category found for this competitor",
                        "reasons": None,
                    })
                    continue

                # Group unique matches by modality
                by_modality: dict[UUID, List[Category]] = {}
                for cat in eligible_cats:
                    if cat.modality.id not in by_modality:
                        by_modality[cat.modality.id] = []
                    by_modality[cat.modality.id].append(cat)

                for modality_id, cats in by_modality.items():
                    if len(cats) == 1:
                        # Exactly one eligible category for this modality
                        registration = CategoryRegistration(
                            id=uuid4(),
                            competitor=competitor,
                            category=cats[0],
                            tournament=tournament,
                        )
                        registrations.append(registration)
                    else:
                        # Conflict: multiple eligible categories for same modality
                        errors.append({
                            "competitor_id": competitor.id,
                            "competitor_name": f"{competitor.first_name} {competitor.last_name}",
                            "message": f"Multiple categories found for modality '{cats[0].modality.name}'. Impossible to choose automatically.",
                            "overlapping_categories": cats,
                            "reasons": None,
                        })

        # 4. Persist each registration
        for registration in registrations:
            await self.registration_repo.create(registration)

        return {"registrations": registrations, "errors": errors}
