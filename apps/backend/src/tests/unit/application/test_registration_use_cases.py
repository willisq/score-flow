import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID
from src.features.registration.application.use_cases import RegistrationUseCases
from src.features.registration.application.schemas import (
    AcademyCreate,
    PersonCreate,
    CompetitorCreate,
    CompetitorFilters,
)
from src.features.registration.domain.entities import Academy, Person, Competitor, Rank, Sex


def test_register_academy_generates_uuids():
    # Arrange
    academy_repo = MagicMock()
    academy_repo.create = AsyncMock(side_effect=lambda x: x)

    use_cases = RegistrationUseCases(
        academy_repo=academy_repo,
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
        competitor_repo=MagicMock(),
    )

    schema = AcademyCreate(
        name="Miyagi-Do",
        instructor=PersonCreate(first_name="Nariyoshi", last_name="Miyagi"),
    )

    # Act
    result = asyncio.run(use_cases.register_academy(schema))

    # Assert
    assert isinstance(result, Academy)
    assert isinstance(result.id, UUID)
    assert isinstance(result.instructor, Person)
    assert isinstance(result.instructor.id, UUID)
    assert result.name == "Miyagi-Do"
    assert result.instructor.first_name == "Nariyoshi"
    assert result.instructor.last_name == "Miyagi"

    # Verify repository was called
    academy_repo.create.assert_called_once()


def test_register_competitor_with_age():
    # Arrange
    academy_repo = MagicMock()
    rank_repo = MagicMock()
    sex_repo = MagicMock()
    competitor_repo = MagicMock()

    academy_id = UUID("12345678-1234-5678-1234-567812345678")
    rank_id = UUID("87654321-4321-8765-4321-876543210987")
    sex_id = UUID("11111111-2222-3333-4444-555555555555")

    academy = Academy(
        id=academy_id,
        name="Cobra Kai",
        instructor=Person(id=UUID(int=1), first_name="Johnny", last_name="Lawrence"),
    )
    rank = Rank(id=rank_id, name="White", classification=1, is_black_belt=False)
    sex = Sex(id=sex_id, name="M")

    academy_repo.get_by_id = AsyncMock(return_value=academy)
    rank_repo.get_by_id = AsyncMock(return_value=rank)
    sex_repo.get_by_id = AsyncMock(return_value=sex)
    competitor_repo.create = AsyncMock(side_effect=lambda x: x)

    use_cases = RegistrationUseCases(
        academy_repo=academy_repo,
        rank_repo=rank_repo,
        sex_repo=sex_repo,
        competitor_repo=competitor_repo,
    )

    schema = CompetitorCreate(
        first_name="Miguel",
        last_name="Diaz",
        academy_id=academy_id,
        rank_id=rank_id,
        sex_id=sex_id,
        weight=65.0,
        height=170.0,
        age=17,
        special_condition=False,
    )

    # Act
    result = asyncio.run(use_cases.register_competitor(schema))

    # Assert
    assert isinstance(result, Competitor)
    assert isinstance(result.id, UUID)
    assert result.first_name == "Miguel"
    assert result.age == 17
    assert result.academy == academy
    competitor_repo.create.assert_called_once()


def test_register_competitor_with_missing_metrics():
    # Arrange
    academy_repo = MagicMock()
    rank_repo = MagicMock()
    sex_repo = MagicMock()
    competitor_repo = MagicMock()

    academy_id = UUID("12345678-1234-5678-1234-567812345678")
    rank_id = UUID("87654321-4321-8765-4321-876543210987")
    sex_id = UUID("11111111-2222-3333-4444-555555555555")

    academy = Academy(
        id=academy_id,
        name="Cobra Kai",
        instructor=Person(id=UUID(int=1), first_name="Johnny", last_name="Lawrence"),
    )
    rank = Rank(id=rank_id, name="White", classification=1, is_black_belt=False)
    sex = Sex(id=sex_id, name="M")

    academy_repo.get_by_id = AsyncMock(return_value=academy)
    rank_repo.get_by_id = AsyncMock(return_value=rank)
    sex_repo.get_by_id = AsyncMock(return_value=sex)
    competitor_repo.create = AsyncMock(side_effect=lambda x: x)

    use_cases = RegistrationUseCases(
        academy_repo=academy_repo,
        rank_repo=rank_repo,
        sex_repo=sex_repo,
        competitor_repo=competitor_repo,
    )

    # Schema with None for weight and height
    schema = CompetitorCreate(
        first_name="Miguel",
        last_name="Diaz",
        academy_id=academy_id,
        rank_id=rank_id,
        sex_id=sex_id,
        weight=None,
        height=None,
        age=17,
        special_condition=False,
    )

    # Act
    result = asyncio.run(use_cases.register_competitor(schema))

    # Assert
    assert isinstance(result, Competitor)
    assert result.weight is None
    assert result.height is None
    competitor_repo.create.assert_called_once()


def test_register_competitors_bulk():
    # Arrange
    academy_repo = MagicMock()
    rank_repo = MagicMock()
    sex_repo = MagicMock()
    competitor_repo = MagicMock()

    academy_id = UUID("12345678-1234-5678-1234-567812345678")
    rank_id = UUID("87654321-4321-8765-4321-876543210987")
    sex_id = UUID("11111111-2222-3333-4444-555555555555")

    academy = Academy(
        id=academy_id,
        name="Cobra Kai",
        instructor=Person(id=UUID(int=1), first_name="Johnny", last_name="Lawrence"),
    )
    rank = Rank(id=rank_id, name="White", classification=1, is_black_belt=False)
    sex = Sex(id=sex_id, name="M")

    academy_repo.get_by_id = AsyncMock(return_value=academy)
    rank_repo.get_by_id = AsyncMock(return_value=rank)
    sex_repo.get_by_id = AsyncMock(return_value=sex)
    competitor_repo.create = AsyncMock(side_effect=lambda x: x)

    use_cases = RegistrationUseCases(
        academy_repo=academy_repo,
        rank_repo=rank_repo,
        sex_repo=sex_repo,
        competitor_repo=competitor_repo,
    )

    schemas = [
        CompetitorCreate(
            first_name="Miguel",
            last_name="Diaz",
            academy_id=academy_id,
            rank_id=rank_id,
            sex_id=sex_id,
        ),
        CompetitorCreate(
            first_name="Robby",
            last_name="Keene",
            academy_id=academy_id,
            rank_id=rank_id,
            sex_id=sex_id,
        ),
    ]

    # Act
    results = asyncio.run(use_cases.register_competitors_bulk(schemas))

    # Assert
    assert len(results) == 2
    assert results[0].first_name == "Miguel"
    assert results[1].first_name == "Robby"
    
    # Verify that dependencies were fetched only once per unique ID
    assert academy_repo.get_by_id.call_count == 1
    assert rank_repo.get_by_id.call_count == 1
    assert sex_repo.get_by_id.call_count == 1
    
    # Verify that create was called for each competitor
    assert competitor_repo.create.call_count == 2


def test_list_competitors_calls_repo_with_filters():
    # Arrange
    competitor_repo = MagicMock()
    competitor_repo.get_all = AsyncMock(return_value=[])

    use_cases = RegistrationUseCases(
        academy_repo=MagicMock(),
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
        competitor_repo=competitor_repo,
    )

    filters = CompetitorFilters(
        name="Diaz",
        academy_id=UUID(int=1),
        rank_id=UUID(int=2),
        sex_id=UUID(int=3),
        special_condition=True,
    )

    # Act
    asyncio.run(use_cases.list_competitors(filters))

    # Assert
    competitor_repo.get_all.assert_called_once_with(
        name="Diaz",
        academy_id=UUID(int=1),
        rank_id=UUID(int=2),
        sex_id=UUID(int=3),
        special_condition=True,
    )
