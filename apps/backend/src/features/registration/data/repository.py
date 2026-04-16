from uuid import UUID

from sqlalchemy import select, func, asc, desc, any_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.features.registration.data.models import (
    AcademyModel,
    CompetitorModel,
    PersonModel,
    RankModel,
    SexModel,
)
from src.features.registration.domain.entities import (
    Academy,
    Competitor,
    Person,
    Rank,
    Sex,
)


class SexRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, sex_id: UUID) -> Sex | None:
        result = await self.session.get(SexModel, sex_id)
        if not result:
            return None
        return Sex(id=result.id, name=result.name)

    async def create(self, sex: Sex) -> Sex:
        model = SexModel(id=sex.id, name=sex.name)
        self.session.add(model)
        return sex

    async def list_all(self) -> list[Sex]:
        result = await self.session.execute(select(SexModel))
        return [Sex(id=m.id, name=m.name) for m in result.scalars().all()]


class RankRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, rank_id: UUID) -> Rank | None:
        result = await self.session.get(RankModel, rank_id)
        if not result:
            return None
        return Rank(
            id=result.id,
            name=result.name,
            classification=result.classification,
            is_black_belt=result.is_black_belt,
        )

    async def create(self, rank: Rank) -> Rank:
        model = RankModel(
            id=rank.id,
            name=rank.name,
            classification=rank.classification,
            is_black_belt=rank.is_black_belt,
        )
        self.session.add(model)
        return rank

    async def list_all(self) -> list[Rank]:
        result = await self.session.execute(select(RankModel))
        return [
            Rank(
                id=m.id,
                name=m.name,
                classification=m.classification,
                is_black_belt=m.is_black_belt,
            )
            for m in result.scalars().all()
        ]


class AcademyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, academy: Academy) -> Academy:
        # Check if instructor (Person) exists, if not create him
        instructor_model = await self.session.get(PersonModel, academy.instructor.id)
        if not instructor_model:
            instructor_model = PersonModel(
                id=academy.instructor.id,
                first_name=academy.instructor.first_name,
                last_name=academy.instructor.last_name,
            )
            self.session.add(instructor_model)

        model = AcademyModel(
            id=academy.id,
            name=academy.name,
            instructor_id=academy.instructor.id,
        )
        self.session.add(model)
        return academy

    async def get_by_id(self, academy_id: UUID) -> Academy | None:
        result = await self.session.execute(
            select(AcademyModel)
            .options(selectinload(AcademyModel.instructor))
            .where(AcademyModel.id == academy_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        instructor = Person(
            id=model.instructor.id,
            first_name=model.instructor.first_name,
            last_name=model.instructor.last_name,
        )
        return Academy(id=model.id, name=model.name, instructor=instructor)

    async def list_all(self) -> list[Academy]:
        result = await self.session.execute(
            select(AcademyModel).options(selectinload(AcademyModel.instructor))
        )
        models = result.scalars().all()
        return [
            Academy(
                id=m.id,
                name=m.name,
                instructor=Person(
                    id=m.instructor.id,
                    first_name=m.instructor.first_name,
                    last_name=m.instructor.last_name,
                ),
            )
            for m in models
        ]


class CompetitorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, competitor: Competitor) -> Competitor:
        # 1. Create or get Person
        person_model = await self.session.get(PersonModel, competitor.id)
        if not person_model:
            person_model = PersonModel(
                id=competitor.id,
                first_name=competitor.first_name,
                last_name=competitor.last_name,
            )
            self.session.add(person_model)

        # 2. Map Competitor
        model = CompetitorModel(
            id=competitor.id,
            person_id=competitor.id,
            academy_id=competitor.academy.id,
            rank_id=competitor.rank.id,
            sex_id=competitor.sex.id,
            weight=competitor.weight,
            height=competitor.height,
            age=competitor.age,
            special_condition=competitor.special_condition,
        )
        self.session.add(model)
        return competitor

    async def get_by_id(self, competitor_id: UUID) -> Competitor | None:
        result = await self.session.execute(
            select(CompetitorModel)
            .options(
                selectinload(CompetitorModel.person),
                selectinload(CompetitorModel.academy).selectinload(
                    AcademyModel.instructor
                ),
                selectinload(CompetitorModel.rank),
                selectinload(CompetitorModel.sex),
            )
            .where(CompetitorModel.id == competitor_id)
        )
        model = result.scalar_one_or_none()
        if not model:
            return None

        academy = Academy(
            id=model.academy.id,
            name=model.academy.name,
            instructor=Person(
                id=model.academy.instructor.id,
                first_name=model.academy.instructor.first_name,
                last_name=model.academy.instructor.last_name,
            ),
        )

        return Competitor(
            id=model.id,
            first_name=model.person.first_name,
            last_name=model.person.last_name,
            academy=academy,
            rank=Rank(
                id=model.rank.id,
                name=model.rank.name,
                classification=model.rank.classification,
                is_black_belt=model.rank.is_black_belt,
            ),
            sex=Sex(id=model.sex.id, name=model.sex.name),
            weight=model.weight,
            height=model.height,
            age=model.age,
            special_condition=model.special_condition,
        )

    async def get_by_ids(self, ids: list[UUID]) -> list[Competitor]:
        stmt = (
            select(CompetitorModel)
            .options(
                selectinload(CompetitorModel.person),
                selectinload(CompetitorModel.academy).selectinload(
                    AcademyModel.instructor
                ),
                selectinload(CompetitorModel.rank),
                selectinload(CompetitorModel.sex),
            )
            .where(CompetitorModel.id.in_(ids))
        )

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [
            Competitor(
                id=m.id,
                first_name=m.person.first_name,
                last_name=m.person.last_name,
                academy=Academy(
                    id=m.academy.id,
                    name=m.academy.name,
                    instructor=Person(
                        id=m.academy.instructor.id,
                        first_name=m.academy.instructor.first_name,
                        last_name=m.academy.instructor.last_name,
                    ),
                ),
                rank=Rank(
                    id=m.rank.id,
                    name=m.rank.name,
                    classification=m.rank.classification,
                    is_black_belt=m.rank.is_black_belt,
                ),
                sex=Sex(id=m.sex.id, name=m.sex.name),
                weight=m.weight,
                height=m.height,
                age=m.age,
                special_condition=m.special_condition,
            )
            for m in models
        ]

    async def get_all(
        self,
        name: str | None = None,
        academy_id: UUID | None = None,
        rank_id: UUID | None = None,
        sex_id: UUID | None = None,
        special_condition: bool | None = None,
    ) -> list[Competitor]:
        from sqlalchemy import or_

        stmt = (
            select(CompetitorModel)
            .join(CompetitorModel.person)
            .options(
                selectinload(CompetitorModel.person),
                selectinload(CompetitorModel.academy).selectinload(
                    AcademyModel.instructor
                ),
                selectinload(CompetitorModel.rank),
                selectinload(CompetitorModel.sex),
            )
        )

        if name:
            search = f"%{name}%"
            stmt = stmt.where(
                or_(
                    PersonModel.first_name.ilike(search),
                    PersonModel.last_name.ilike(search),
                )
            )

        if academy_id:
            stmt = stmt.where(CompetitorModel.academy_id == academy_id)
        if rank_id:
            stmt = stmt.where(CompetitorModel.rank_id == rank_id)
        if sex_id:
            stmt = stmt.where(CompetitorModel.sex_id == sex_id)
        if special_condition is not None:
            stmt = stmt.where(CompetitorModel.special_condition == special_condition)

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [
            Competitor(
                id=m.id,
                first_name=m.person.first_name,
                last_name=m.person.last_name,
                academy=Academy(
                    id=m.academy.id,
                    name=m.academy.name,
                    instructor=Person(
                        id=m.academy.instructor.id,
                        first_name=m.academy.instructor.first_name,
                        last_name=m.academy.instructor.last_name,
                    ),
                ),
                rank=Rank(
                    id=m.rank.id,
                    name=m.rank.name,
                    classification=m.rank.classification,
                    is_black_belt=m.rank.is_black_belt,
                ),
                sex=Sex(id=m.sex.id, name=m.sex.name),
                weight=m.weight,
                height=m.height,
                age=m.age,
                special_condition=m.special_condition,
            )
            for m in models
        ]

    async def get_all_for_category_builder(
        self,
        min_age: int | None = None,
        max_age: int | None = None,
        rank_ids: list[UUID] | None = None,
        sex_ids: list[UUID] | None = None,
        special_condition: bool | None = None,
    ) -> list[Competitor]:
        stmt = (
            select(CompetitorModel)
            .join(CompetitorModel.person)
            .options(
                selectinload(CompetitorModel.person),
                selectinload(CompetitorModel.academy).selectinload(
                    AcademyModel.instructor
                ),
                selectinload(CompetitorModel.rank),
                selectinload(CompetitorModel.sex),
            )
        )
 
        if min_age is not None:
            stmt = stmt.where(CompetitorModel.age >= min_age)
        if max_age is not None:
            stmt = stmt.where(CompetitorModel.age <= max_age)
        if rank_ids:
            stmt = stmt.where(CompetitorModel.rank_id.in_(rank_ids))
        if sex_ids:
            stmt = stmt.where(CompetitorModel.sex_id.in_(sex_ids))
        if special_condition is not None:
            stmt = stmt.where(CompetitorModel.special_condition == special_condition)
 
        # Default sorting by age and weight (asc)
        stmt = stmt.order_by(asc(CompetitorModel.age), asc(CompetitorModel.weight))

        result = await self.session.execute(stmt)
        models = result.scalars().all()

        return [
            Competitor(
                id=m.id,
                first_name=m.person.first_name,
                last_name=m.person.last_name,
                academy=Academy(
                    id=m.academy.id,
                    name=m.academy.name,
                    instructor=Person(
                        id=m.academy.instructor.id,
                        first_name=m.academy.instructor.first_name,
                        last_name=m.academy.instructor.last_name,
                    ),
                ),
                rank=Rank(
                    id=m.rank.id,
                    name=m.rank.name,
                    classification=m.rank.classification,
                    is_black_belt=m.rank.is_black_belt,
                ),
                sex=Sex(id=m.sex.id, name=m.sex.name),
                weight=m.weight,
                height=m.height,
                age=m.age,
                special_condition=m.special_condition,
            )
            for m in models
        ]

    async def get_filter_options(self) -> dict:
        # Get distinct ages
        ages_stmt = (
            select(func.distinct(CompetitorModel.age))
            .where(CompetitorModel.age.is_not(None))
            .order_by(CompetitorModel.age)
        )
        ages_result = await self.session.execute(ages_stmt)
        ages = [r for r in ages_result.scalars().all()]

        # Get ranks present in competitors
        ranks_stmt = select(RankModel).where(
            RankModel.id.in_(select(CompetitorModel.rank_id))
        )
        ranks_result = await self.session.execute(ranks_stmt)
        ranks = [
            Rank(
                id=m.id,
                name=m.name,
                classification=m.classification,
                is_black_belt=m.is_black_belt,
            )
            for m in ranks_result.scalars().all()
        ]

        # Get sexes present in competitors
        sexes_stmt = select(SexModel).where(
            SexModel.id.in_(select(CompetitorModel.sex_id))
        )
        sexes_result = await self.session.execute(sexes_stmt)
        sexes = [Sex(id=m.id, name=m.name) for m in sexes_result.scalars().all()]

        # Check if special condition exists
        special_stmt = select(func.count(CompetitorModel.id)).where(
            CompetitorModel.special_condition.is_(True)
        )
        special_result = await self.session.execute(special_stmt)
        has_special = special_result.scalar() > 0

        return {
            "ages": ages,
            "ranks": ranks,
            "sexes": sexes,
            "has_special_condition": has_special,
        }
