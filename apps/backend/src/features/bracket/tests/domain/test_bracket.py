import pytest
from uuid import uuid4
from src.core.common.exceptions import DomainException
from src.features.bracket.domain.entities import Round, Match
from src.features.bracket.domain.errors import BracketError
from src.features.registration.domain.entities import (
    Competitor,
    Academy,
    Person,
    Rank,
    Sex,
)


@pytest.fixture
def valid_id():
    return uuid4()


@pytest.fixture
def valid_competitor(valid_id):
    # Mocking minimal dependencies for competitor
    instructor = Person(id=valid_id, first_name="Sensei", last_name="X")
    academy = Academy(id=valid_id, name="Dojo", instructor=instructor)
    rank = Rank(id=valid_id, name="White", is_black_belt=False)
    sex = Sex(id=valid_id, name="Male")
    
    return Competitor(
        id=valid_id,
        first_name="John",
        last_name="Doe",
        academy=academy,
        rank=rank,
        sex=sex,
        weight=70.0,
        height=170.0,
        special_condition=False,
    )


@pytest.fixture
def valid_round(valid_id):
    return Round(id=valid_id, description="Finals")


class TestRound:
    def test_valid_creation(self, valid_id):
        round_entity = Round(id=valid_id, description="Semi-Finals")
        assert round_entity.description == "Semi-Finals"

    def test_invalid_description(self, valid_id):
        with pytest.raises(DomainException) as exc:
            Round(id=valid_id, description="")
        assert exc.value.code == BracketError.INVALID_ROUND_DESCRIPTION.code


class TestMatch:
    def test_valid_creation(self, valid_id, valid_round):
        match = Match(id=valid_id, round=valid_round)
        assert match.round == valid_round
        assert match.winner is None

    def test_set_winner_success(self, valid_id, valid_round, valid_competitor):
        competitor_2 = Competitor(
            id=uuid4(),
            first_name="Jane",
            last_name="Doe",
            academy=valid_competitor.academy,
            rank=valid_competitor.rank,
            sex=valid_competitor.sex,
            weight=65.0,
            height=165.0,
            special_condition=False,
        )
        
        match = Match(
            id=valid_id,
            round=valid_round,
            first_competitor=valid_competitor,
            second_competitor=competitor_2,
        )
        
        match.set_winner(valid_competitor)
        assert match.winner == valid_competitor

    def test_set_winner_invalid_competitor(self, valid_id, valid_round, valid_competitor):
        match = Match(
            id=valid_id,
            round=valid_round,
            first_competitor=valid_competitor,
            second_competitor=None, # Bye or empty slot
        )
        
        # Trying to set a winner that is not part of the match (even if it's the same object instance, logic checks presence)
        # Creating a distinct competitor
        outsider = Competitor(
            id=uuid4(),
            first_name="Outsider",
            last_name="Player",
            academy=valid_competitor.academy,
            rank=valid_competitor.rank,
            sex=valid_competitor.sex,
            weight=80.0,
            height=180.0,
            special_condition=False,
        )

        with pytest.raises(DomainException) as exc:
            match.set_winner(outsider)
        assert exc.value.code == BracketError.INVALID_MATCH_WINNER.code
