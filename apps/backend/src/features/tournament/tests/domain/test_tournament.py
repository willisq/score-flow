import pytest
from uuid import uuid4
from src.core.common.exceptions import DomainException
from src.features.tournament.domain.entities import (
    Modality,
    Tournament,
    Category,
)
from src.features.tournament.domain.errors import TournamentError
from src.features.registration.domain.entities import Sex, Rank


@pytest.fixture
def valid_id():
    return uuid4()


@pytest.fixture
def valid_modality(valid_id):
    return Modality(id=valid_id, name="Sparring")


@pytest.fixture
def valid_sex(valid_id):
    return Sex(id=valid_id, name="Male")


@pytest.fixture
def valid_rank(valid_id):
    return Rank(id=valid_id, name="Black Belt", is_black_belt=True)


class TestModality:
    def test_valid_creation(self, valid_id):
        modality = Modality(id=valid_id, name="Forms")
        assert modality.name == "Forms"

    def test_invalid_name(self, valid_id):
        with pytest.raises(DomainException) as exc:
            Modality(id=valid_id, name="")
        assert exc.value.code == TournamentError.INVALID_MODALITY_NAME.code


class TestTournament:
    def test_valid_creation(self, valid_id):
        tournament = Tournament(id=valid_id, description="National Championship")
        assert tournament.description == "National Championship"

    def test_invalid_description(self, valid_id):
        with pytest.raises(DomainException) as exc:
            Tournament(id=valid_id, description="")
        assert exc.value.code == TournamentError.INVALID_TOURNAMENT_DESCRIPTION.code


class TestCategory:
    def test_valid_creation(
        self, valid_id, valid_modality, valid_sex, valid_rank
    ):
        category = Category(
            id=valid_id,
            name="Elite Male -70kg",
            initial_age=18,
            final_age=35,
            special_condition=False,
            modality=valid_modality,
            sexes=[valid_sex],
            ranks=[valid_rank],
            initial_weight=60.0,
            final_weight=70.0,
        )
        assert category.name == "Elite Male -70kg"
        assert category.modality == valid_modality

    def test_invalid_name(self, valid_id, valid_modality, valid_sex, valid_rank):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                name="",
                initial_age=18,
                final_age=35,
                special_condition=False,
                modality=valid_modality,
                sexes=[valid_sex],
                ranks=[valid_rank],
            )
        assert exc.value.code == TournamentError.INVALID_CATEGORY_NAME.code

    def test_invalid_modality(self, valid_id, valid_sex, valid_rank):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                name="Test Category",
                initial_age=18,
                final_age=35,
                special_condition=False,
                modality=None,  # type: ignore
                sexes=[valid_sex],
                ranks=[valid_rank],
            )
        assert exc.value.code == TournamentError.INVALID_CATEGORY_MODALITY.code

    @pytest.mark.parametrize("age", [-1, -5])
    def test_invalid_age_limits(
        self, valid_id, valid_modality, valid_sex, valid_rank, age
    ):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id, name="Test", initial_age=age, final_age=10,
                special_condition=False, modality=valid_modality, sexes=[valid_sex], ranks=[valid_rank]
            )
        assert exc.value.code == TournamentError.INVALID_AGE_LIMITS.code

    def test_invalid_age_range(self, valid_id, valid_modality, valid_sex, valid_rank):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id, name="Test", initial_age=20, final_age=10, # Initial > Final
                special_condition=False, modality=valid_modality, sexes=[valid_sex], ranks=[valid_rank]
            )
        assert exc.value.code == TournamentError.INVALID_AGE_RANGE.code
