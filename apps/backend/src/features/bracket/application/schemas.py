from typing import List, Optional
from uuid import UUID
from pydantic import Field

from src.core.common.models import TunedModel
from src.features.registration.application.schemas import CompetitorSchema


class GenerateBracketsRequest(TunedModel):
    category_modality_ids: Optional[List[UUID]] = Field(
        default=None, 
        description="Lista opcional de IDs de category_modality para armar rondas. Si está vacío o es None, usa todas las categorías activas."
    )


class GeneratedCategoryResult(TunedModel):
    category_modality_id: UUID
    matches_generated: int
    

class GenerateBracketsResponse(TunedModel):
    results: List[GeneratedCategoryResult]


class RoundSchema(TunedModel):
    id: UUID
    description: str


class MatchSchema(TunedModel):
    id: UUID
    round: RoundSchema
    position: int
    category_modality_id: Optional[UUID] = None
    first_competitor: CompetitorSchema
    second_competitor: Optional[CompetitorSchema] = None
    winner: Optional[CompetitorSchema] = None


class RemoveCompetitorRequest(TunedModel):
    category_modality_id: UUID
    registration_id: UUID
