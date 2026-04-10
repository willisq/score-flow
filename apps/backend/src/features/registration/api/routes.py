import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.features.registration.application.excel_processor import ExcelCompetitorProcessor
from src.features.registration.application.schemas import (
    AcademyCreate,
    AcademySchema,
    CompetitorBulkCreate,
    CompetitorCreate,
    CompetitorFilters,
    CompetitorSchema,
    RankCreate,
    RankSchema,
    SexCreate,
    SexSchema,
)
from src.features.registration.application.use_cases import RegistrationUseCases
from src.features.registration.data.repository import (
    AcademyRepository,
    CompetitorRepository,
    RankRepository,
    SexRepository,
)

router = APIRouter(prefix="/registration", tags=["Registration"])


def get_registration_use_cases(
    session: AsyncSession = Depends(get_db),
) -> RegistrationUseCases:
    return RegistrationUseCases(
        academy_repo=AcademyRepository(session),
        rank_repo=RankRepository(session),
        sex_repo=SexRepository(session),
        competitor_repo=CompetitorRepository(session),
    )


@router.post("/sexes", response_model=SexSchema)
async def create_sex(
    schema: SexCreate,
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    result = await use_cases.register_sex(schema)
    await use_cases.sex_repo.session.commit()
    return result


@router.get("/sexes", response_model=list[SexSchema])
async def list_sexes(
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    return await use_cases.list_sexes()


@router.post("/ranks", response_model=RankSchema)
async def create_rank(
    schema: RankCreate,
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    result = await use_cases.register_rank(schema)
    await use_cases.rank_repo.session.commit()
    return result


@router.get("/ranks", response_model=list[RankSchema])
async def list_ranks(
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    return await use_cases.list_ranks()


@router.post("/academies", response_model=AcademySchema)
async def create_academy(
    schema: AcademyCreate,
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    result = await use_cases.register_academy(schema)
    await use_cases.academy_repo.session.commit()
    return result


@router.get("/academies", response_model=list[AcademySchema])
async def list_academies(
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    return await use_cases.list_academies()


@router.post(
    "/competitors", response_model=CompetitorSchema, status_code=status.HTTP_201_CREATED
)
async def create_competitor(
    schema: CompetitorCreate,
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    try:
        result = await use_cases.register_competitor(schema)
        await use_cases.competitor_repo.session.commit()

        return await use_cases.competitor_repo.get_by_id(result.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/competitors/bulk",
    response_model=list[CompetitorSchema],
    status_code=status.HTTP_201_CREATED,
)
async def create_competitors_bulk(
    schema: CompetitorBulkCreate,
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    try:
        results = await use_cases.register_competitors_bulk(schema.competitors)
        await use_cases.competitor_repo.session.commit()
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


@router.get("/competitors", response_model=list[CompetitorSchema])
async def list_competitors(
    filters: CompetitorFilters = Depends(),
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    return await use_cases.list_competitors(filters)


@router.post(
    "/competitors/upload",
    response_model=list[CompetitorSchema],
    status_code=status.HTTP_201_CREATED,
)
async def upload_competitors(
    file: UploadFile = File(...),
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    """
    Ruta para el registro masivo de competidores mediante un archivo Excel.
    """
    try:
        # 1. Procesar Excel y convertirlo en esquemas
        schemas = await ExcelCompetitorProcessor.process_excel(file, use_cases)

        # 2. Registrar competidores en bloque
        results = await use_cases.register_competitors_bulk(schemas)

        # 3. Confirmar transacción
        await use_cases.competitor_repo.session.commit()

        return results
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al procesar el archivo Excel: {str(e)}",
        )


@router.get("/competitors/template")
async def download_template():
    """
    Ruta para descargar la plantilla de Excel para el registro masivo de competidores.
    """
    current_dir = os.path.dirname(__file__)
    template_path = os.path.join(current_dir, "templates", "competitor_template.xlsx")

    if not os.path.exists(template_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plantilla de Excel no encontrada.",
        )

    return FileResponse(
        path=template_path,
        filename="plantilla_competidores.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
