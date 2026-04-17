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


class PhysicalRequirementCreate(TunedModel):
    initial_weight: Optional[float] = Field(default=None, ge=0)
    final_weight: Optional[float] = Field(default=None, ge=0)
    initial_height: Optional[float] = Field(default=None, ge=0)
    final_height: Optional[float] = Field(default=None, ge=0)


class CategoryModalityCreate(TunedModel):
    modality_id: UUID
    physical_requirement: Optional[PhysicalRequirementCreate] = None


class CategoryCreate(TunedModel):
    ages: List[int]
    special_condition: bool = False
    rank_ids: List[UUID]
    sex_ids: List[UUID]
    modalities: List[CategoryModalityCreate]


class CategoryUpdate(TunedModel):
    ages: Optional[List[int]] = None
    special_condition: Optional[bool] = None
    rank_ids: Optional[List[UUID]] = None
    sex_ids: Optional[List[UUID]] = None
    modalities: Optional[List[CategoryModalityCreate]] = None


class PhysicalRequirementSchema(TunedModel):
    id: UUID
    initial_weight: Optional[float] = None
    final_weight: Optional[float] = None
    initial_height: Optional[float] = None
    final_height: Optional[float] = None


class CategoryModalitySchema(TunedModel):
    id: UUID
    modality: ModalitySchema
    physical_requirement: Optional[PhysicalRequirementSchema] = None
    # Flattened from Category for easier UI access
    ages: List[int] = []
    sexes: List[SexSchema] = []
    ranks: List[RankSchema] = []


class CategorySchema(TunedModel):
    id: UUID
    ages: List[int]
    special_condition: bool
    ranks: List[RankSchema]
    sexes: List[SexSchema]
    modalities: List[CategoryModalitySchema]


class CategoryRegistrationCreate(TunedModel):
    competitor_id: UUID
    category_modality_id: UUID
    tournament_id: UUID


class CategoryRegistrationSchema(TunedModel):
    id: UUID
    competitor: CompetitorSchema
    category_modality: CategoryModalitySchema
    tournament: TournamentSchema


class RegistrationErrorSchema(TunedModel):
    competitor_id: UUID
    competitor_name: str
    message: str
    reasons: Optional[dict[str, bool]] = None
    overlapping_categories: Optional[List[CategorySchema]] = None


class MassRegistrationResponse(TunedModel):
    registrations: List[CategoryRegistrationSchema]
    errors: List[RegistrationErrorSchema]


class MassRegistrationRequest(TunedModel):
    competitor_ids: List[UUID]
    tournament_id: UUID
    category_modality_id: Optional[UUID] = None


class CategoryBulkCreate(TunedModel):
    categories: List[CategoryCreate]
