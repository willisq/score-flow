from uuid import UUID
import os
from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.features.registration.application.excel_processor import (
    ExcelCompetitorProcessor,
)
from src.features.registration.application.schemas import (
    AcademyCreate,
    AcademySchema,
    CompetitorBulkCreate,
    CompetitorCreate,
    CompetitorFilters,
    CompetitorCategoryFilters,
    CompetitorFilterOptions,
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


@router.put("/competitors/{competitor_id}", response_model=CompetitorSchema)
async def update_competitor(
    competitor_id: UUID,
    schema: CompetitorCreate,
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    try:
        result = await use_cases.update_competitor(competitor_id, schema)
        await use_cases.competitor_repo.session.commit()
        return await use_cases.competitor_repo.get_by_id(result.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
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


@router.get("/competitors/filter-options", response_model=CompetitorFilterOptions)
async def get_competitor_filter_options(
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    return await use_cases.get_competitor_filter_options()


@router.get("/competitors/for-category-builder", response_model=list[CompetitorSchema])
async def list_competitors_for_category_builder(
    filters: Annotated[CompetitorCategoryFilters, Query()],
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    return await use_cases.list_competitors_for_category_builder(filters)


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
async def download_template(
    use_cases: RegistrationUseCases = Depends(get_registration_use_cases),
):
    """
    Ruta para descargar la plantilla de Excel para el registro masivo de competidores.
    """
    try:
        from src.features.registration.application.excel_template_generator import (
            ExcelTemplateGenerator,
        )

        # Consultar listas de base de datos
        sexes_schemas = await use_cases.list_sexes()
        ranks_schemas = await use_cases.list_ranks()
        academies_schemas = await use_cases.list_academies()

        sexes = [s.name for s in sexes_schemas]
        ranks = [r.name for r in ranks_schemas]
        academies = [a.name for a in academies_schemas]

        # Generar buffer del template dinámico
        buffer = ExcelTemplateGenerator.generate_dynamic_template(
            academies=academies, ranks=ranks, sexes=sexes
        )

        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=plantilla_competidores.xlsx"
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar la plantilla: {str(e)}",
        )
