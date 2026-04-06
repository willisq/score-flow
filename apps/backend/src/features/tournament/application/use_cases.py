from uuid import uuid4
from typing import List

from src.features.tournament.application.schemas import (
    ModalityCreate,
    TournamentCreate,
    CategoryCreate,
    CategoryRegistrationCreate,
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
            name=schema.name,
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
