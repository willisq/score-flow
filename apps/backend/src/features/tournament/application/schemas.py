from uuid import UUID
from typing import List, Optional
from pydantic import Field

from src.core.common.models import TunedModel
from src.features.registration.application.schemas import RankSchema, SexSchema, CompetitorSchema


class ModalityCreate(TunedModel):
    name: str


class ModalitySchema(TunedModel):
    id: UUID
    name: str


class TournamentCreate(TunedModel):
    description: str


class TournamentSchema(TunedModel):
    id: UUID
    description: str


class CategoryCreate(TunedModel):
    ages: List[int]
    special_condition: bool = False
    modality_id: UUID
    rank_ids: List[UUID]
    sex_ids: List[UUID]
    initial_weight: Optional[float] = Field(default=None, ge=0)
    final_weight: Optional[float] = Field(default=None, ge=0)
    initial_height: Optional[float] = Field(default=None, ge=0)
    final_height: Optional[float] = Field(default=None, ge=0)


class CategorySchema(TunedModel):
    id: UUID
    ages: List[int]
    special_condition: bool
    modality: ModalitySchema
    ranks: List[RankSchema]
    sexes: List[SexSchema]
    initial_weight: Optional[float] = None
    final_weight: Optional[float] = None
    initial_height: Optional[float] = None
    final_height: Optional[float] = None


class CategoryRegistrationCreate(TunedModel):
    competitor_id: UUID
    category_id: UUID
    tournament_id: UUID


class CategoryRegistrationSchema(TunedModel):
    id: UUID
    competitor: CompetitorSchema
    category: CategorySchema
    tournament: TournamentSchema
