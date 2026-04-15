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
from src.features.tournament.application.schemas import (
    CategoryCreate,
    CategoryRegistrationCreate,
    MassRegistrationRequest,
    ModalityCreate,
    TournamentCreate,
)
from src.features.tournament.application.use_cases import TournamentUseCases
from src.features.tournament.domain.entities import (
    Category,
    CategoryRegistration,
    Modality,
    Tournament,
)


def test_register_modality():
    modality_repo = MagicMock()
    modality_repo.create = AsyncMock(side_effect=lambda x: x)
    
    use_cases = TournamentUseCases(
        modality_repo=modality_repo,
        tournament_repo=MagicMock(),
        category_repo=MagicMock(),
        registration_repo=MagicMock(),
        competitor_repo=MagicMock(),
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
    )
    
    schema = ModalityCreate(name="Kyorugi")
    result = asyncio.run(use_cases.register_modality(schema))
    
    assert isinstance(result, Modality)
    assert result.name == "Kyorugi"
    modality_repo.create.assert_called_once()


def test_register_tournament():
    tournament_repo = MagicMock()
    tournament_repo.create = AsyncMock(side_effect=lambda x: x)
    
    use_cases = TournamentUseCases(
        modality_repo=MagicMock(),
        tournament_repo=tournament_repo,
        category_repo=MagicMock(),
        registration_repo=MagicMock(),
        competitor_repo=MagicMock(),
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
    )
    
    schema = TournamentCreate(description="Open Panamericano")
    result = asyncio.run(use_cases.register_tournament(schema))
    
    assert isinstance(result, Tournament)
    assert result.description == "Open Panamericano"
    tournament_repo.create.assert_called_once()


def test_register_category():
    modality_repo = MagicMock()
    rank_repo = MagicMock()
    sex_repo = MagicMock()
    category_repo = MagicMock()
    
    modality1 = Modality(id=uuid4(), name="Sparring")
    modality2 = Modality(id=uuid4(), name="Poomsae")
    rank = Rank(id=uuid4(), name="Black", classification=10, is_black_belt=True)
    sex = Sex(id=uuid4(), name="Male")
    
    async def get_modality_by_id(mid):
        if mid == modality1.id: return modality1
        if mid == modality2.id: return modality2
        return None
        
    modality_repo.get_by_id = AsyncMock(side_effect=get_modality_by_id)
    rank_repo.get_by_id = AsyncMock(return_value=rank)
    sex_repo.get_by_id = AsyncMock(return_value=sex)
    category_repo.create = AsyncMock(side_effect=lambda x: x)
    
    use_cases = TournamentUseCases(
        modality_repo=modality_repo,
        tournament_repo=MagicMock(),
        category_repo=category_repo,
        registration_repo=MagicMock(),
        competitor_repo=MagicMock(),
        rank_repo=rank_repo,
        sex_repo=sex_repo,
    )
    
    schema = CategoryCreate(
        ages=[18, 40],
        modality_ids=[modality1.id, modality2.id],
        rank_ids=[rank.id],
        sex_ids=[sex.id],
        initial_weight=80.0,
        final_weight=120.0
    )
    
    results = asyncio.run(use_cases.register_category(schema))
    
    assert isinstance(results, list)
    assert len(results) == 2
    assert results[0].modality == modality1
    assert results[1].modality == modality2
    assert rank in results[0].ranks
    assert sex in results[0].sexes
    assert category_repo.create.call_count == 2


def test_inscribe_competitor():
    competitor_repo = MagicMock()
    category_repo = MagicMock()
    tournament_repo = MagicMock()
    registration_repo = MagicMock()
    
    # Setup objects
    instructor = Person(id=uuid4(), first_name="Nariyoshi", last_name="Miyagi")
    academy = Academy(id=uuid4(), name="Miyagi-Do", instructor=instructor)
    rank = Rank(id=uuid4(), name="White", classification=1, is_black_belt=False)
    sex = Sex(id=uuid4(), name="Male")
    
    competitor = Competitor(
        id=uuid4(), first_name="Daniel", last_name="LaRusso", 
        academy=academy, rank=rank, sex=sex
    )
    
    modality = Modality(id=uuid4(), name="Sparring")
    category = Category(
        id=uuid4(), ages=[15, 17], 
        special_condition=False,
        modality=modality, ranks=[rank], sexes=[sex]
    )
    
    tournament = Tournament(id=uuid4(), description="All Valley")
    
    competitor_repo.get_by_id = AsyncMock(return_value=competitor)
    category_repo.get_by_id = AsyncMock(return_value=category)
    tournament_repo.get_by_id = AsyncMock(return_value=tournament)
    registration_repo.create = AsyncMock(side_effect=lambda x: x)
    
    use_cases = TournamentUseCases(
        modality_repo=MagicMock(),
        tournament_repo=tournament_repo,
        category_repo=category_repo,
        registration_repo=registration_repo,
        competitor_repo=competitor_repo,
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
    )
    
    schema = CategoryRegistrationCreate(
        competitor_id=competitor.id,
        category_id=category.id,
        tournament_id=tournament.id
    )
    
    result = asyncio.run(use_cases.inscribe_competitor(schema))
    
    assert isinstance(result, CategoryRegistration)
    assert result.competitor == competitor
    assert result.category == category
    assert result.tournament == tournament
    registration_repo.create.assert_called_once()


def test_mass_register_competitors():
    tournament_repo = MagicMock()
    category_repo = MagicMock()
    competitor_repo = MagicMock()
    registration_repo = MagicMock()
    
    # Setup
    tournament = Tournament(id=uuid4(), description="Mass Test")
    modality = Modality(id=uuid4(), name="Mass Modality")
    rank = Rank(id=uuid4(), name="White", classification=1, is_black_belt=False)
    sex = Sex(id=uuid4(), name="Male")
    
    category = Category(
        id=uuid4(), ages=[18], special_condition=False,
        modality=modality, ranks=[rank], sexes=[sex]
    )
    
    instructor = Person(id=uuid4(), first_name="Nariyoshi", last_name="Miyagi")
    academy = Academy(id=uuid4(), name="Miyagi-Do", instructor=instructor)
    competitor = Competitor(
        id=uuid4(), first_name="Daniel", last_name="LaRusso",
        academy=academy, rank=rank, sex=sex, age=18
    )
    
    tournament_repo.get_by_id = AsyncMock(return_value=tournament)
    category_repo.list_all = AsyncMock(return_value=[category])
    competitor_repo.get_by_ids = AsyncMock(return_value=[competitor])
    registration_repo.create = AsyncMock(side_effect=lambda x: x)
    
    use_cases = TournamentUseCases(
        modality_repo=MagicMock(),
        tournament_repo=tournament_repo,
        category_repo=category_repo,
        registration_repo=registration_repo,
        competitor_repo=competitor_repo,
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
    )
    
    schema = MassRegistrationRequest(
        competitor_ids=[competitor.id],
        tournament_id=tournament.id
    )
    
    result = asyncio.run(use_cases.mass_register_competitors(schema))
    
    assert len(result["registrations"]) == 1
    assert result["registrations"][0].competitor == competitor
    assert result["registrations"][0].category == category
    assert len(result["errors"]) == 0
    registration_repo.create.assert_called_once()


def test_mass_register_competitors_with_category_id():
    tournament_repo = MagicMock()
    category_repo = MagicMock()
    competitor_repo = MagicMock()
    registration_repo = MagicMock()

    # Setup
    tournament = Tournament(id=uuid4(), description="Manual Mass Test")
    modality = Modality(id=uuid4(), name="Mass Modality")
    rank = Rank(id=uuid4(), name="White", classification=1, is_black_belt=False)
    sex = Sex(id=uuid4(), name="Male")

    category = Category(
        id=uuid4(), ages=[18], special_condition=False,
        modality=modality, ranks=[rank], sexes=[sex]
    )

    instructor = Person(id=uuid4(), first_name="Nariyoshi", last_name="Miyagi")
    academy = Academy(id=uuid4(), name="Miyagi-Do", instructor=instructor)
    competitor = Competitor(
        id=uuid4(), first_name="Daniel", last_name="LaRusso",
        academy=academy, rank=rank, sex=sex, age=18
    )

    tournament_repo.get_by_id = AsyncMock(return_value=tournament)
    category_repo.get_by_id = AsyncMock(return_value=category)
    competitor_repo.get_by_ids = AsyncMock(return_value=[competitor])
    registration_repo.create = AsyncMock(side_effect=lambda x: x)

    use_cases = TournamentUseCases(
        modality_repo=MagicMock(),
        tournament_repo=tournament_repo,
        category_repo=category_repo,
        registration_repo=registration_repo,
        competitor_repo=competitor_repo,
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
    )

    schema = MassRegistrationRequest(
        competitor_ids=[competitor.id],
        tournament_id=tournament.id,
        category_id=category.id
    )

    result = asyncio.run(use_cases.mass_register_competitors(schema))

    assert len(result["registrations"]) == 1
    assert result["registrations"][0].competitor == competitor
    assert result["registrations"][0].category == category
    assert result["registrations"][0].tournament == tournament
    assert len(result["errors"]) == 0
    registration_repo.create.assert_called_once()
    category_repo.get_by_id.assert_called_once_with(category.id)


def test_mass_register_competitors_with_category_id_invalid():
    tournament_repo = MagicMock()
    category_repo = MagicMock()
    competitor_repo = MagicMock()
    registration_repo = MagicMock()

    # Setup
    tournament = Tournament(id=uuid4(), description="Manual Mass Test Invalid")
    modality = Modality(id=uuid4(), name="Mass Modality")
    rank = Rank(id=uuid4(), name="White", classification=1, is_black_belt=False)
    sex = Sex(id=uuid4(), name="Male")

    category = Category(
        id=uuid4(), ages=[18], special_condition=False,
        modality=modality, ranks=[rank], sexes=[sex]
    )

    instructor = Person(id=uuid4(), first_name="Nariyoshi", last_name="Miyagi")
    academy = Academy(id=uuid4(), name="Miyagi-Do", instructor=instructor)
    # Competitor is 20, but category is for 18
    competitor = Competitor(
        id=uuid4(), first_name="Daniel", last_name="LaRusso",
        academy=academy, rank=rank, sex=sex, age=20
    )

    tournament_repo.get_by_id = AsyncMock(return_value=tournament)
    category_repo.get_by_id = AsyncMock(return_value=category)
    competitor_repo.get_by_ids = AsyncMock(return_value=[competitor])

    use_cases = TournamentUseCases(
        modality_repo=MagicMock(),
        tournament_repo=tournament_repo,
        category_repo=category_repo,
        registration_repo=registration_repo,
        competitor_repo=competitor_repo,
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
    )

    schema = MassRegistrationRequest(
        competitor_ids=[competitor.id],
        tournament_id=tournament.id,
        category_id=category.id,
    )

    result = asyncio.run(use_cases.mass_register_competitors(schema))

    assert len(result["registrations"]) == 0
    assert len(result["errors"]) == 1
    error = result["errors"][0]
    assert error["competitor_id"] == competitor.id
    assert error["reasons"]["age_mismatch"] is True
    assert "not eligible" in error["message"]
    registration_repo.create.assert_not_called()


def test_mass_register_competitors_overlapping_modalities():
    tournament_repo = MagicMock()
    category_repo = MagicMock()
    competitor_repo = MagicMock()
    registration_repo = MagicMock()

    # Setup
    tournament = Tournament(id=uuid4(), description="Overlapping Test")
    modality = Modality(id=uuid4(), name="Sparring")
    rank = Rank(id=uuid4(), name="White", classification=1, is_black_belt=False)
    sex = Sex(id=uuid4(), name="Male")

    # Two categories for the SAME modality that both fit
    cat1 = Category(
        id=uuid4(), ages=[18], special_condition=False,
        modality=modality, ranks=[rank], sexes=[sex]
    )
    cat2 = Category(
        id=uuid4(), ages=[18], special_condition=False,
        modality=modality, ranks=[rank], sexes=[sex]
    )

    instructor = Person(id=uuid4(), first_name="Nariyoshi", last_name="Miyagi")
    academy = Academy(id=uuid4(), name="Miyagi-Do", instructor=instructor)
    competitor = Competitor(
        id=uuid4(), first_name="Daniel", last_name="LaRusso",
        academy=academy, rank=rank, sex=sex, age=18
    )

    tournament_repo.get_by_id = AsyncMock(return_value=tournament)
    category_repo.list_all = AsyncMock(return_value=[cat1, cat2])
    competitor_repo.get_by_ids = AsyncMock(return_value=[competitor])

    use_cases = TournamentUseCases(
        modality_repo=MagicMock(),
        tournament_repo=tournament_repo,
        category_repo=category_repo,
        registration_repo=registration_repo,
        competitor_repo=competitor_repo,
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
    )

    schema = MassRegistrationRequest(
        competitor_ids=[competitor.id],
        tournament_id=tournament.id
    )

    result = asyncio.run(use_cases.mass_register_competitors(schema))

    assert len(result["registrations"]) == 0
    assert len(result["errors"]) == 1
    assert "Multiple categories found" in result["errors"][0]["message"]
    assert result["errors"][0]["overlapping_categories"] == [cat1, cat2]
    registration_repo.create.assert_not_called()
