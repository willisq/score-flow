import asyncio
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from src.features.tournament.application.use_cases import TournamentUseCases
from src.features.tournament.application.schemas import (
    ModalityCreate,
    TournamentCreate,
    CategoryCreate,
    CategoryRegistrationCreate,
)
from src.features.tournament.domain.entities import Modality, Tournament, Category, CategoryRegistration
from src.features.registration.domain.entities import Competitor, Rank, Sex, Person, Academy


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
    
    modality = Modality(id=uuid4(), name="Sparring")
    rank = Rank(id=uuid4(), name="Black", classification=10, is_black_belt=True)
    sex = Sex(id=uuid4(), name="Male")
    
    modality_repo.get_by_id = AsyncMock(return_value=modality)
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
        name="Senior Male Heavyweight",
        ages=[18, 40],
        modality_id=modality.id,
        rank_ids=[rank.id],
        sex_ids=[sex.id],
        initial_weight=80.0,
        final_weight=120.0
    )
    
    result = asyncio.run(use_cases.register_category(schema))
    
    assert isinstance(result, Category)
    assert result.name == "Senior Male Heavyweight"
    assert result.modality == modality
    assert rank in result.ranks
    assert sex in result.sexes
    category_repo.create.assert_called_once()


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
        id=uuid4(), name="Test Category", ages=[15, 17], 
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
