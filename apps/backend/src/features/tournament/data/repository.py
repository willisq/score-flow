from uuid import UUID, uuid4
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.features.tournament.data.models import (
    ModalityModel,
    TournamentModel,
    CategoryModel,
    CategoryModalityModel,
    PhysicalRequirementModel,
    CategoryRegistrationModel,
    RankGroupModel,
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
from src.features.registration.domain.entities import Competitor, Rank, Sex, Person, Academy
from src.features.registration.data.models import CompetitorModel, RankModel, SexModel, AcademyModel


class ModalityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, modality: Modality) -> Modality:
        model = ModalityModel(id=modality.id, name=modality.name)
        self.session.add(model)
        return modality

    async def get_by_id(self, modality_id: UUID) -> Optional[Modality]:
        result = await self.session.get(ModalityModel, modality_id)
        if not result:
            return None
        return Modality(id=result.id, name=result.name)

    async def list_all(self) -> List[Modality]:
        result = await self.session.execute(select(ModalityModel))
        return [Modality(id=m.id, name=m.name) for m in result.scalars().all()]


class TournamentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tournament: Tournament) -> Tournament:
        model = TournamentModel(id=tournament.id, description=tournament.description)
        self.session.add(model)
        return tournament

    async def get_by_id(self, tournament_id: UUID) -> Optional[Tournament]:
        result = await self.session.get(TournamentModel, tournament_id)
        if not result:
            return None
        return Tournament(id=result.id, description=result.description)

    async def list_all(self) -> List[Tournament]:
        result = await self.session.execute(select(TournamentModel))
        return [Tournament(id=m.id, description=m.description) for m in result.scalars().all()]


class RankGroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, rank_group: RankGroup) -> RankGroup:
        model = RankGroupModel(id=rank_group.id, name=rank_group.name)
        for rank in rank_group.ranks:
            r_model = await self.session.get(RankModel, rank.id)
            if r_model:
                model.ranks.append(r_model)
        self.session.add(model)
        return rank_group

    async def get_by_id(self, group_id: UUID) -> Optional[RankGroup]:
        stmt = select(RankGroupModel).options(selectinload(RankGroupModel.ranks)).where(RankGroupModel.id == group_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return RankGroup(
            id=model.id,
            name=model.name,
            ranks=[
                Rank(id=r.id, name=r.name, classification=r.classification, is_black_belt=r.is_black_belt)
                for r in model.ranks
            ]
        )

    async def list_all(self) -> List[RankGroup]:
        stmt = select(RankGroupModel).options(selectinload(RankGroupModel.ranks))
        result = await self.session.execute(stmt)
        return [
            RankGroup(
                id=m.id,
                name=m.name,
                ranks=[
                    Rank(id=r.id, name=r.name, classification=r.classification, is_black_belt=r.is_black_belt)
                    for r in m.ranks
                ]
            )
            for m in result.scalars().all()
        ]

    async def get_model_by_id(self, group_id: UUID) -> Optional[RankGroupModel]:
        stmt = select(RankGroupModel).options(selectinload(RankGroupModel.ranks)).where(RankGroupModel.id == group_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, group_id: UUID) -> bool:
        model = await self.session.get(RankGroupModel, group_id)
        if not model:
            return False
        await self.session.delete(model)
        return True


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_physical_requirement(
        self,
        initial_weight: Optional[float],
        final_weight: Optional[float],
        initial_height: Optional[float],
        final_height: Optional[float],
        preferred_id: Optional[UUID] = None
    ) -> PhysicalRequirementModel:
        # Try to find existing
        stmt = select(PhysicalRequirementModel).where(
            PhysicalRequirementModel.initial_weight == initial_weight,
            PhysicalRequirementModel.final_weight == final_weight,
            PhysicalRequirementModel.initial_height == initial_height,
            PhysicalRequirementModel.final_height == final_height,
        )
        result = await self.session.execute(stmt)
        existing = result.scalars().first()
        
        if existing:
            return existing
            
        # Create new
        new_pr = PhysicalRequirementModel(
            id=preferred_id or uuid4(),
            initial_weight=initial_weight,
            final_weight=final_weight,
            initial_height=initial_height,
            final_height=final_height,
        )
        self.session.add(new_pr)
        return new_pr

    async def create(self, category: Category) -> Category:
        model = CategoryModel(
            id=category.id,
            ages=category.ages,
            special_condition=category.special_condition,
        )

        # Add modalities and their physical requirements / rank groups
        for cat_mod in category.modalities:
            # 1. Handle Physical Requirement
            pr_id = None
            if cat_mod.physical_requirement:
                pr = cat_mod.physical_requirement
                pr_model = await self.get_or_create_physical_requirement(
                    pr.initial_weight,
                    pr.final_weight,
                    pr.initial_height,
                    pr.final_height,
                    preferred_id=pr.id
                )
                pr_id = pr_model.id

            # 2. Handle Rank Group
            rank_group_id = None
            if cat_mod.rank_group:
                rg = cat_mod.rank_group
                # Check if group already exists (simple check by ID if provided, 
                # or we could implement a deep check)
                existing_rg = await self.session.get(RankGroupModel, rg.id)
                if not existing_rg:
                    rg_model = RankGroupModel(id=rg.id, name=rg.name)
                    for r in rg.ranks:
                        r_model = await self.session.get(RankModel, r.id)
                        if r_model:
                            rg_model.ranks.append(r_model)
                    self.session.add(rg_model)
                    rank_group_id = rg_model.id
                else:
                    rank_group_id = existing_rg.id

            mod_model = CategoryModalityModel(
                id=cat_mod.id,
                category_id=category.id,
                modality_id=cat_mod.modality.id,
                rank_group_id=rank_group_id,
                physical_requirement_id=pr_id,
            )
            for sex in cat_mod.sexes:
                sex_model = await self.session.get(SexModel, sex.id)
                if sex_model:
                    mod_model.sexes.append(sex_model)
            model.modalities.append(mod_model)

        self.session.add(model)
        return category

    async def get_model_by_id(self, category_id: UUID) -> Optional[CategoryModel]:
        stmt = (
            select(CategoryModel)
            .options(
                selectinload(CategoryModel.modalities).selectinload(CategoryModalityModel.modality),
                selectinload(CategoryModel.modalities).selectinload(CategoryModalityModel.sexes),
                selectinload(CategoryModel.modalities).selectinload(CategoryModalityModel.rank_group).selectinload(RankGroupModel.ranks),
                selectinload(CategoryModel.modalities).selectinload(CategoryModalityModel.physical_requirement),
            )
            .where(CategoryModel.id == category_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, category_id: UUID) -> Optional[Category]:
        model = await self.get_model_by_id(category_id)
        if not model:
            return None

        return self._to_domain(model)

    async def list_all(self) -> List[Category]:
        stmt = select(CategoryModel).options(
            selectinload(CategoryModel.modalities).selectinload(CategoryModalityModel.modality),
            selectinload(CategoryModel.modalities).selectinload(CategoryModalityModel.sexes),
            selectinload(CategoryModel.modalities).selectinload(CategoryModalityModel.rank_group).selectinload(RankGroupModel.ranks),
            selectinload(CategoryModel.modalities).selectinload(CategoryModalityModel.physical_requirement),
        )
        result = await self.session.execute(stmt)
        return [self._to_domain(m) for m in result.scalars().all()]

    async def get_modality_model_by_id(self, modality_id: UUID) -> Optional[CategoryModalityModel]:
        stmt = (
            select(CategoryModalityModel)
            .options(
                selectinload(CategoryModalityModel.modality),
                selectinload(CategoryModalityModel.sexes),
                selectinload(CategoryModalityModel.rank_group).selectinload(RankGroupModel.ranks),
                selectinload(CategoryModalityModel.physical_requirement),
                selectinload(CategoryModalityModel.category),
            )
            .where(CategoryModalityModel.id == modality_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_modality_by_id(self, modality_id: UUID) -> Optional[CategoryModality]:
        model = await self.get_modality_model_by_id(modality_id)
        if not model:
            return None

        # Return domain entity
        category = Category(
            id=model.category.id,
            ages=model.category.ages,
            special_condition=model.category.special_condition,
        )
        
        rank_group = None
        if model.rank_group:
            rank_group = RankGroup(
                id=model.rank_group.id,
                name=model.rank_group.name,
                ranks=[
                    Rank(id=r.id, name=r.name, classification=r.classification, is_black_belt=r.is_black_belt)
                    for r in model.rank_group.ranks
                ]
            )

        return CategoryModality(
            id=model.id,
            category=category,
            modality=Modality(id=model.modality.id, name=model.modality.name),
            sexes=[Sex(id=s.id, name=s.name) for s in model.sexes],
            rank_group=rank_group,
            physical_requirement=PhysicalRequirement(
                id=model.physical_requirement.id,
                initial_weight=model.physical_requirement.initial_weight,
                final_weight=model.physical_requirement.final_weight,
                initial_height=model.physical_requirement.initial_height,
                final_height=model.physical_requirement.final_height,
            ) if model.physical_requirement else None
        )

    def _to_domain(self, model: CategoryModel) -> Category:
        category = Category(
            id=model.id,
            ages=model.ages,
            special_condition=model.special_condition,
        )

        category.modalities = [
            CategoryModality(
                id=m.id,
                category=category,
                modality=Modality(id=m.modality.id, name=m.modality.name),
                sexes=[Sex(id=s.id, name=s.name) for s in m.sexes],
                rank_group=RankGroup(
                    id=m.rank_group.id,
                    name=m.rank_group.name,
                    ranks=[
                        Rank(id=r.id, name=r.name, classification=r.classification, is_black_belt=r.is_black_belt)
                        for r in m.rank_group.ranks
                    ]
                ) if m.rank_group else None,
                physical_requirement=PhysicalRequirement(
                    id=m.physical_requirement.id,
                    initial_weight=m.physical_requirement.initial_weight,
                    final_weight=m.physical_requirement.final_weight,
                    initial_height=m.physical_requirement.initial_height,
                    final_height=m.physical_requirement.final_height,
                ) if m.physical_requirement else None
            )
            for m in model.modalities
        ]
        return category


class CategoryRegistrationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, registration: CategoryRegistration) -> CategoryRegistration:
        model = CategoryRegistrationModel(
            id=registration.id,
            competitor_id=registration.competitor.id,
            category_modality_id=registration.category_modality.id,
            tournament_id=registration.tournament.id,
        )
        self.session.add(model)
        return registration

    async def get_by_id(self, registration_id: UUID) -> Optional[CategoryRegistration]:
        stmt = (
            select(CategoryRegistrationModel)
            .options(
                # Load competitor and its relations
                selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.person),
                selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.academy).selectinload(AcademyModel.instructor),
                selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.rank),
                selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.sex),
                # Load category_modality and its relations
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.modality),
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.sexes),
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.rank_group).selectinload(RankGroupModel.ranks),
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.physical_requirement),
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.category),
                # Load tournament
                selectinload(CategoryRegistrationModel.tournament),
            )
            .where(CategoryRegistrationModel.id == registration_id)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None

        # Deep mapping to Domain
        competitor_model = model.competitor
        academy_model = competitor_model.academy

        academy = Academy(
            id=academy_model.id,
            name=academy_model.name,
            instructor=Person(
                id=academy_model.instructor.id,
                first_name=academy_model.instructor.first_name,
                last_name=academy_model.instructor.last_name
            )
        )

        competitor = Competitor(
            id=competitor_model.id,
            first_name=competitor_model.person.first_name,
            last_name=competitor_model.person.last_name,
            academy=academy,
            rank=Rank(
                id=competitor_model.rank.id,
                name=competitor_model.rank.name,
                classification=competitor_model.rank.classification,
                is_black_belt=competitor_model.rank.is_black_belt
            ),
            sex=Sex(id=competitor_model.sex.id, name=competitor_model.sex.name),
            weight=competitor_model.weight,
            height=competitor_model.height,
            age=competitor_model.age,
            special_condition=competitor_model.special_condition
        )

        cat_model = model.category_modality.category
        category = Category(
            id=cat_model.id,
            ages=cat_model.ages,
            special_condition=cat_model.special_condition,
        )

        mod_model = model.category_modality
        
        rank_group = None
        if mod_model.rank_group:
            rank_group = RankGroup(
                id=mod_model.rank_group.id,
                name=mod_model.rank_group.name,
                ranks=[
                    Rank(id=r.id, name=r.name, classification=r.classification, is_black_belt=r.is_black_belt)
                    for r in mod_model.rank_group.ranks
                ]
            )

        category_modality = CategoryModality(
            id=mod_model.id,
            category=category,
            modality=Modality(id=mod_model.modality.id, name=mod_model.modality.name),
            sexes=[Sex(id=s.id, name=s.name) for s in mod_model.sexes],
            rank_group=rank_group,
            physical_requirement=PhysicalRequirement(
                id=mod_model.physical_requirement.id,
                initial_weight=mod_model.physical_requirement.initial_weight,
                final_weight=mod_model.physical_requirement.final_weight,
                initial_height=mod_model.physical_requirement.initial_height,
                final_height=mod_model.physical_requirement.final_height
            ) if mod_model.physical_requirement else None
        )

        tournament = Tournament(
            id=model.tournament.id,
            description=model.tournament.description
        )

        return CategoryRegistration(
            id=model.id,
            competitor=competitor,
            category_modality=category_modality,
            tournament=tournament
        )

    async def get_by_categories(self, category_modality_ids: Optional[List[UUID]] = None) -> List[CategoryRegistration]:
        stmt = (
            select(CategoryRegistrationModel)
            .options(
                selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.person),
                selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.academy).selectinload(AcademyModel.instructor),
                selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.rank),
                selectinload(CategoryRegistrationModel.competitor).selectinload(CompetitorModel.sex),
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.modality),
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.sexes),
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.rank_group).selectinload(RankGroupModel.ranks),
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.physical_requirement),
                selectinload(CategoryRegistrationModel.category_modality).selectinload(CategoryModalityModel.category),
                selectinload(CategoryRegistrationModel.tournament),
            )
        )

        if category_modality_ids:
            stmt = stmt.where(CategoryRegistrationModel.category_modality_id.in_(category_modality_ids))

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        registrations = []
        for model in models:
            # Reutilizando el mapeo de get_by_id
            competitor_model = model.competitor
            academy_model = competitor_model.academy

            academy = Academy(
                id=academy_model.id,
                name=academy_model.name,
                instructor=Person(
                    id=academy_model.instructor.id,
                    first_name=academy_model.instructor.first_name,
                    last_name=academy_model.instructor.last_name
                )
            )

            competitor = Competitor(
                id=competitor_model.id,
                first_name=competitor_model.person.first_name,
                last_name=competitor_model.person.last_name,
                academy=academy,
                rank=Rank(
                    id=competitor_model.rank.id,
                    name=competitor_model.rank.name,
                    classification=competitor_model.rank.classification,
                    is_black_belt=competitor_model.rank.is_black_belt
                ),
                sex=Sex(id=competitor_model.sex.id, name=competitor_model.sex.name),
                weight=competitor_model.weight,
                height=competitor_model.height,
                age=competitor_model.age,
                special_condition=competitor_model.special_condition
            )

            cat_model = model.category_modality.category
            category = Category(
                id=cat_model.id,
                ages=cat_model.ages,
                special_condition=cat_model.special_condition,
            )

            mod_model = model.category_modality
            
            rank_group = None
            if mod_model.rank_group:
                rank_group = RankGroup(
                    id=mod_model.rank_group.id,
                    name=mod_model.rank_group.name,
                    ranks=[
                        Rank(id=r.id, name=r.name, classification=r.classification, is_black_belt=r.is_black_belt)
                        for r in mod_model.rank_group.ranks
                    ]
                )

            category_modality = CategoryModality(
                id=mod_model.id,
                category=category,
                modality=Modality(id=mod_model.modality.id, name=mod_model.modality.name),
                sexes=[Sex(id=s.id, name=s.name) for s in mod_model.sexes],
                rank_group=rank_group,
                physical_requirement=PhysicalRequirement(
                    id=mod_model.physical_requirement.id,
                    initial_weight=mod_model.physical_requirement.initial_weight,
                    final_weight=mod_model.physical_requirement.final_weight,
                    initial_height=mod_model.physical_requirement.initial_height,
                    final_height=mod_model.physical_requirement.final_height
                ) if mod_model.physical_requirement else None
            )

            tournament = Tournament(
                id=model.tournament.id,
                description=model.tournament.description
            )

            registrations.append(CategoryRegistration(
                id=model.id,
                competitor=competitor,
                category_modality=category_modality,
                tournament=tournament
            ))

        return registrations
