from uuid import UUID

from pydantic import Field, field_validator

from src.core.common.models import TunedModel


class SexCreate(TunedModel):
    name: str


class SexSchema(TunedModel):
    id: UUID
    name: str


class RankCreate(TunedModel):
    name: str
    classification: int
    is_black_belt: bool


class RankSchema(TunedModel):
    id: UUID
    name: str
    classification: int
    is_black_belt: bool


class PersonSchema(TunedModel):
    id: UUID
    first_name: str
    last_name: str


class PersonCreate(TunedModel):
    first_name: str
    last_name: str


class AcademyCreate(TunedModel):
    name: str
    instructor: PersonCreate


class AcademySchema(TunedModel):
    id: UUID
    name: str
    instructor: PersonSchema


class CompetitorCreate(TunedModel):
    first_name: str
    last_name: str
    academy_id: UUID
    rank_id: UUID
    sex_id: UUID
    weight: float | None = Field(default=None, gt=0)
    height: float | None = Field(default=None, gt=0)
    age: int | None = None
    special_condition: bool = False


class CompetitorBulkCreate(TunedModel):
    competitors: list[CompetitorCreate]


class CompetitorSchema(TunedModel):
    id: UUID
    first_name: str
    last_name: str
    academy: AcademySchema
    rank: RankSchema
    sex: SexSchema
    weight: float | None = None
    height: float | None = None
    age: int | None = None
    special_condition: bool


class CompetitorFilters(TunedModel):
    name: str | None = None
    academy_id: UUID | None = None
    rank_id: UUID | None = None
    sex_id: UUID | None = None
    special_condition: bool | None = None


class CompetitorCategoryFilters(TunedModel):
    min_age: int | None = None
    max_age: int | None = None
    rank_ids: list[UUID] | None = None
    sex_ids: list[UUID] | None = None
    special_condition: bool | None = None
    sort_by: str | None = None  # age, weight
    sort_order: str | None = "asc"  # asc, desc


class CompetitorFilterOptions(TunedModel):
    ages: list[int]
    ranks: list[RankSchema]
    sexes: list[SexSchema]
    has_special_condition: bool
