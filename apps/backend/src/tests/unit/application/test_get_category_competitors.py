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
from src.features.tournament.application.use_cases import TournamentUseCases
from src.features.tournament.domain.entities import (
    Category,
    CategoryModality,
    CategoryRegistration,
    Modality,
    Tournament,
)


def test_get_competitors_by_category_modality():
    registration_repo = MagicMock()
    
    # Setup objects
    instructor = Person(id=uuid4(), first_name="Nariyoshi", last_name="Miyagi")
    academy = Academy(id=uuid4(), name="Miyagi-Do", instructor=instructor)
    rank = Rank(id=uuid4(), name="White", classification=1, is_black_belt=False)
    sex = Sex(id=uuid4(), name="Male")
    
    competitor1 = Competitor(
        id=uuid4(), first_name="Daniel", last_name="LaRusso", 
        academy=academy, rank=rank, sex=sex
    )
    competitor2 = Competitor(
        id=uuid4(), first_name="Johnny", last_name="Lawrence", 
        academy=academy, rank=rank, sex=sex
    )
    
    modality = Modality(id=uuid4(), name="Sparring")
    category = Category(
        id=uuid4(), ages=[15, 17], 
        special_condition=False,
        sexes=[sex]
    )
    cat_mod = CategoryModality(id=uuid4(), category=category, modality=modality)
    category.modalities.append(cat_mod)
    
    tournament = Tournament(id=uuid4(), description="All Valley")
    
    reg1 = CategoryRegistration(id=uuid4(), competitor=competitor1, category_modality=cat_mod, tournament=tournament)
    reg2 = CategoryRegistration(id=uuid4(), competitor=competitor2, category_modality=cat_mod, tournament=tournament)
    
    registration_repo.get_by_categories = AsyncMock(return_value=[reg1, reg2])
    
    use_cases = TournamentUseCases(
        modality_repo=MagicMock(),
        tournament_repo=MagicMock(),
        category_repo=MagicMock(),
        registration_repo=registration_repo,
        competitor_repo=MagicMock(),
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
        rank_group_repo=MagicMock(),
    )
    
    result = asyncio.run(use_cases.get_competitors_by_category_modality(cat_mod.id))
    
    assert isinstance(result, list)
    assert len(result) == 2
    assert competitor1 in result
    assert competitor2 in result
    registration_repo.get_by_categories.assert_called_once_with([cat_mod.id])
