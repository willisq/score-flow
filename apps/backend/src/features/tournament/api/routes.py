from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.features.tournament.application.schemas import (
    ModalityCreate,
    ModalitySchema,
    TournamentCreate,
    TournamentSchema,
    CategoryCreate,
    CategorySchema,
    CategoryRegistrationCreate,
    CategoryRegistrationSchema,
    MassRegistrationRequest,
    MassRegistrationResponse,
    CompetitorSchema,
)
from src.features.tournament.application.use_cases import TournamentUseCases
from src.features.tournament.data.repository import (
    ModalityRepository,
    TournamentRepository,
    CategoryRepository,
    CategoryRegistrationRepository,
)
from src.features.registration.data.repository import (
    CompetitorRepository,
    RankRepository,
    SexRepository,
)

router = APIRouter(prefix="/tournament", tags=["Tournament"])


def get_tournament_use_cases(
    session: AsyncSession = Depends(get_db),
) -> TournamentUseCases:
    return TournamentUseCases(
        modality_repo=ModalityRepository(session),
        tournament_repo=TournamentRepository(session),
        category_repo=CategoryRepository(session),
        registration_repo=CategoryRegistrationRepository(session),
        competitor_repo=CompetitorRepository(session),
        rank_repo=RankRepository(session),
        sex_repo=SexRepository(session),
    )


@router.post(
    "/modalities", response_model=ModalitySchema, status_code=status.HTTP_201_CREATED
)
async def create_modality(
    schema: ModalityCreate,
    use_cases: TournamentUseCases = Depends(get_tournament_use_cases),
):
    result = await use_cases.register_modality(schema)
    await use_cases.modality_repo.session.commit()
    return result


@router.get("/modalities", response_model=list[ModalitySchema])
async def list_modalities(
    use_cases: TournamentUseCases = Depends(get_tournament_use_cases),
):
    return await use_cases.list_modalities()


@router.post(
    "/tournaments", response_model=TournamentSchema, status_code=status.HTTP_201_CREATED
)
async def create_tournament(
    schema: TournamentCreate,
    use_cases: TournamentUseCases = Depends(get_tournament_use_cases),
):
    result = await use_cases.register_tournament(schema)
    await use_cases.tournament_repo.session.commit()
    return result


@router.get("/tournaments", response_model=list[TournamentSchema])
async def list_tournaments(
    use_cases: TournamentUseCases = Depends(get_tournament_use_cases),
):
    return await use_cases.list_tournaments()


@router.post(
    "/categories",
    response_model=list[CategorySchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    schema: CategoryCreate,
    use_cases: TournamentUseCases = Depends(get_tournament_use_cases),
):
    try:
        results = await use_cases.register_category(schema)
        await use_cases.category_repo.session.commit()
        # To ensure all relations are loaded
        return [await use_cases.category_repo.get_by_id(res.id) for res in results]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/categories", response_model=list[CategorySchema])
async def list_categories(
    use_cases: TournamentUseCases = Depends(get_tournament_use_cases),
):
    return await use_cases.list_categories()


@router.post(
    "/inscriptions",
    response_model=CategoryRegistrationSchema,
    status_code=status.HTTP_201_CREATED,
)
async def inscribe_competitor(
    schema: CategoryRegistrationCreate,
    use_cases: TournamentUseCases = Depends(get_tournament_use_cases),
):
    try:
        result = await use_cases.inscribe_competitor(schema)
        await use_cases.registration_repo.session.commit()
        # Ensure deep reload for response mapping
        return await use_cases.registration_repo.get_by_id(result.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.post(
    "/mass-registration",
    response_model=MassRegistrationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def mass_register_competitors(
    schema: MassRegistrationRequest,
    use_cases: TournamentUseCases = Depends(get_tournament_use_cases),
):
    try:
        result = await use_cases.mass_register_competitors(schema)
        await use_cases.registration_repo.session.commit()

        # Reload successful registrations for complete response model mapping
        registrations = [
            await use_cases.registration_repo.get_by_id(reg.id)
            for reg in result["registrations"]
        ]

        return {"registrations": registrations, "errors": result["errors"]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.get(
    "/categories/{category_id}/competitors", response_model=list[CompetitorSchema]
)
async def get_category_competitors(
    category_id: UUID,
    use_cases: TournamentUseCases = Depends(get_tournament_use_cases),
):
    try:
        return await use_cases.get_competitors_by_category(category_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
