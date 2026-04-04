import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID
from src.features.registration.application.use_cases import RegistrationUseCases
from src.features.registration.application.schemas import AcademyCreate, PersonCreate
from src.features.registration.domain.entities import Academy, Person

def test_register_academy_generates_uuids():
    # Arrange
    academy_repo = MagicMock()
    academy_repo.create = AsyncMock(side_effect=lambda x: x)
    
    use_cases = RegistrationUseCases(
        academy_repo=academy_repo,
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
        competitor_repo=MagicMock()
    )
    
    schema = AcademyCreate(
        name="Miyagi-Do",
        instructor=PersonCreate(
            first_name="Nariyoshi",
            last_name="Miyagi"
        )
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
