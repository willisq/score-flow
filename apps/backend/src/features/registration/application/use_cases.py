from uuid import uuid4

from src.features.registration.application.schemas import (
    AcademyCreate,
    CompetitorCreate,
    CompetitorFilters,
    RankCreate,
    SexCreate,
)
from src.features.registration.data.repository import (
    AcademyRepository,
    CompetitorRepository,
    RankRepository,
    SexRepository,
)
from src.features.registration.domain.entities import (
    Academy,
    Competitor,
    Person,
    Rank,
    Sex,
)


class RegistrationUseCases:
    def __init__(
        self,
        academy_repo: AcademyRepository,
        rank_repo: RankRepository,
        sex_repo: SexRepository,
        competitor_repo: CompetitorRepository,
    ):
        self.academy_repo = academy_repo
        self.rank_repo = rank_repo
        self.sex_repo = sex_repo
        self.competitor_repo = competitor_repo

    async def register_sex(self, schema: SexCreate) -> Sex:
        sex = Sex(id=uuid4(), name=schema.name)
        return await self.sex_repo.create(sex)

    async def register_rank(self, schema: RankCreate) -> Rank:
        rank = Rank(
            id=uuid4(),
            name=schema.name,
            classification=schema.classification,
            is_black_belt=schema.is_black_belt,
        )
        return await self.rank_repo.create(rank)

    async def register_academy(self, schema: AcademyCreate) -> Academy:
        instructor = Person(
            id=uuid4(),
            first_name=schema.instructor.first_name,
            last_name=schema.instructor.last_name,
        )
        academy = Academy(
            id=uuid4(),
            name=schema.name,
            instructor=instructor,
        )
        return await self.academy_repo.create(academy)

    async def register_competitor(self, schema: CompetitorCreate) -> Competitor:
        # 1. Fetch dependencies (Academy, Rank, Sex) to ensure they exist and build the Domain object
        academy = await self.academy_repo.get_by_id(schema.academy_id)
        if not academy:
            raise ValueError(f"Academy with ID {schema.academy_id} not found")

        rank = await self.rank_repo.get_by_id(schema.rank_id)
        if not rank:
            raise ValueError(f"Rank with ID {schema.rank_id} not found")

        sex = await self.sex_repo.get_by_id(schema.sex_id)
        if not sex:
            raise ValueError(f"Sex with ID {schema.sex_id} not found")

        # 2. Create Domain Entity (Validation happens in __post_init__)
        competitor = Competitor(
            id=uuid4(),
            first_name=schema.first_name,
            last_name=schema.last_name,
            academy=academy,
            rank=rank,
            sex=sex,
            weight=schema.weight,
            height=schema.height,
            age=schema.age,
            special_condition=schema.special_condition,
        )

        return await self.competitor_repo.create(competitor)

    async def list_academies(self) -> list[Academy]:
        return await self.academy_repo.list_all()

    async def list_ranks(self) -> list[Rank]:
        return await self.rank_repo.list_all()

    async def list_sexes(self) -> list[Sex]:
        return await self.sex_repo.list_all()

    async def list_competitors(self, filters: CompetitorFilters) -> list[Competitor]:
        return await self.competitor_repo.get_all(
            name=filters.name,
            academy_id=filters.academy_id,
            rank_id=filters.rank_id,
            sex_id=filters.sex_id,
            special_condition=filters.special_condition,
        )
