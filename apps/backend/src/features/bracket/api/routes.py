from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from src.core.database import get_db
from src.features.bracket.application.schemas import GenerateBracketsRequest, GenerateBracketsResponse, MatchSchema
from src.features.bracket.application.use_cases import BracketUseCases
from src.features.bracket.data.repository import BracketRepository, RoundRepository
from src.features.tournament.data.repository import CategoryRegistrationRepository

router = APIRouter(prefix="/pyramid", tags=["Brackets"])


def get_bracket_use_cases(
    session: AsyncSession = Depends(get_db)
) -> BracketUseCases:
    return BracketUseCases(
        bracket_repo=BracketRepository(session),
        round_repo=RoundRepository(session),
        registration_repo=CategoryRegistrationRepository(session)
    )


@router.post(
    "/generate",
    response_model=GenerateBracketsResponse,
    status_code=status.HTTP_201_CREATED
)
async def generate_brackets(
    request: GenerateBracketsRequest,
    use_cases: BracketUseCases = Depends(get_bracket_use_cases)
):
    try:
        results = await use_cases.generate_initial_brackets(request)
        await use_cases.bracket_repo.session.commit()
        return GenerateBracketsResponse(results=results)
    except Exception as e:
        await use_cases.bracket_repo.session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/",
    response_model=List[MatchSchema]
)
async def get_brackets(
    category_modality_ids: Optional[List[UUID]] = Query(None, description="Filtrar por IDs de category_modality"),
    rounds: Optional[List[UUID]] = Query(None, description="Filtrar por IDs de rondas"),
    rank_id: Optional[UUID] = Query(None, description="Filtrar por ID de rango"),
    age: Optional[int] = Query(None, description="Filtrar por edad contenida en la categoría"),
    modality_id: Optional[UUID] = Query(None, description="Filtrar por ID de modalidad"),
    special_condition: Optional[bool] = Query(None, description="Filtrar por condición especial"),
    weight: Optional[float] = Query(None, description="Filtrar por peso (dentro del rango de requermientos)"),
    use_cases: BracketUseCases = Depends(get_bracket_use_cases)
):
    try:
        return await use_cases.get_brackets(
            categories=category_modality_ids, 
            rounds=rounds,
            rank_id=rank_id,
            age=age,
            modality_id=modality_id,
            special_condition=special_condition,
            weight=weight
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
