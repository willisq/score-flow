import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.features.registration.domain.entities import (
    Academy,
    Competitor,
    Person,
    Rank,
    Sex,
)
from src.features.registration.application.schemas import (
    CompetitorCategoryFilters,
)
from src.features.registration.application.use_cases import RegistrationUseCases
from src.features.tournament.application.schemas import (
    CategoryCreate,
    CategoryBulkCreate,
    CategoryModalityCreate,
    PhysicalRequirementCreate,
)
from src.features.tournament.application.use_cases import TournamentUseCases
from src.features.tournament.domain.entities import (
    Category,
    Modality,
)


def test_register_categories_bulk():
    # Arrange
    modality_repo = MagicMock()
    rank_repo = MagicMock()
    sex_repo = MagicMock()
    category_repo = MagicMock()
    rank_group_repo = MagicMock()
    
    modality = Modality(id=uuid4(), name="Sparring")
    rank = Rank(id=uuid4(), name="Black", classification=10, is_black_belt=True)
    sex = Sex(id=uuid4(), name="Male")
    rank_group_id = uuid4()
    
    modality_repo.get_by_id = AsyncMock(return_value=modality)
    rank_repo.get_by_id = AsyncMock(return_value=rank)
    sex_repo.get_by_id = AsyncMock(return_value=sex)
    category_repo.create = AsyncMock(side_effect=lambda x: x)
    from src.features.tournament.data.models import PhysicalRequirementModel
    category_repo.get_or_create_physical_requirement = AsyncMock(
        side_effect=lambda iw, fw, ih, fh: PhysicalRequirementModel(
            id=uuid4(), initial_weight=iw, final_weight=fw, initial_height=ih, final_height=fh
        )
    )
    
    from src.features.tournament.domain.entities import RankGroup
    rank_group_repo.get_by_id = AsyncMock(
        return_value=RankGroup(id=rank_group_id, name="Avanzados", ranks=[rank])
    )
    
    use_cases = TournamentUseCases(
        modality_repo=modality_repo,
        tournament_repo=MagicMock(),
        category_repo=category_repo,
        registration_repo=MagicMock(),
        competitor_repo=MagicMock(),
        rank_repo=rank_repo,
        sex_repo=sex_repo,
        rank_group_repo=rank_group_repo,
    )
    
    schema = CategoryBulkCreate(
        categories=[
            CategoryCreate(
                ages=[18, 40],
                modalities=[
                    CategoryModalityCreate(
                        modality_id=modality.id,
                        sex_ids=[sex.id],
                        rank_group_ids=[rank_group_id],
                        physical_requirements=[
                            PhysicalRequirementCreate(
                                initial_weight=80.0,
                                final_weight=120.0
                            )
                        ]
                    )
                ]
            ),
            CategoryCreate(
                ages=[10, 15],
                modalities=[
                    CategoryModalityCreate(
                        modality_id=modality.id,
                        sex_ids=[sex.id],
                        rank_group_ids=[rank_group_id],
                        physical_requirements=[
                            PhysicalRequirementCreate(
                                initial_weight=40.0,
                                final_weight=60.0
                            )
                        ]
                    )
                ]
            )
        ]
    )
    
    # Act
    results = asyncio.run(use_cases.register_categories_bulk(schema))
    
    # Assert
    assert len(results) == 2
    assert results[0].ages == [18, 40]
    assert results[1].ages == [10, 15]
    assert category_repo.create.call_count == 2


def test_list_competitors_for_category_builder():
    # Arrange
    competitor_repo = MagicMock()
    use_cases = RegistrationUseCases(
        academy_repo=MagicMock(),
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
        competitor_repo=competitor_repo,
    )
    
    filters = CompetitorCategoryFilters(
        min_age=10,
        max_age=20,
        rank_ids=[uuid4()],
        sex_ids=[uuid4()],
        special_condition=False,
    )
    
    competitor_repo.get_all_for_category_builder = AsyncMock(return_value=[])
    
    # Act
    asyncio.run(use_cases.list_competitors_for_category_builder(filters))
    
    # Assert
    competitor_repo.get_all_for_category_builder.assert_called_once_with(
        min_age=10,
        max_age=20,
        rank_ids=filters.rank_ids,
        sex_ids=filters.sex_ids,
        special_condition=False,
    )


def test_get_competitor_filter_options():
    # Arrange
    competitor_repo = MagicMock()
    use_cases = RegistrationUseCases(
        academy_repo=MagicMock(),
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
        competitor_repo=competitor_repo,
    )
    
    expected_options = {
        "ages": [10, 11, 12],
        "ranks": [],
        "sexes": [],
        "has_special_condition": True
    }
    competitor_repo.get_filter_options = AsyncMock(return_value=expected_options)
    
    # Act
    result = asyncio.run(use_cases.get_competitor_filter_options())
    
    # Assert
    assert result == expected_options
    competitor_repo.get_filter_options.assert_called_once()
