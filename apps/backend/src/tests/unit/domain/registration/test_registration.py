import pytest
from src.core.common.exceptions import DomainException
from src.features.registration.domain.entities import (
    Sex,
    Person,
    Academy,
    Rank,
    Competitor,
)
from src.features.registration.domain.errors import RegistrationError


@pytest.fixture
def valid_instructor(valid_id):
    return Person(id=valid_id, first_name="Sensei", last_name="Miyagi")


@pytest.fixture
def valid_academy(valid_id, valid_instructor):
    return Academy(id=valid_id, name="Cobra Kai", instructor=valid_instructor)


class TestSex:
    def test_valid_creation(self, valid_id):
        sex = Sex(id=valid_id, name="Female")
        assert sex.name == "Female"

    def test_invalid_name(self, valid_id):
        with pytest.raises(DomainException) as exc:
            Sex(id=valid_id, name="")
        assert exc.value.code == RegistrationError.INVALID_SEX_NAME.code


class TestPerson:
    def test_valid_creation(self, valid_id):
        person = Person(id=valid_id, first_name="Jane", last_name="Doe")
        assert person.full_name == "Jane Doe"

    def test_invalid_first_name(self, valid_id):
        with pytest.raises(DomainException) as exc:
            Person(id=valid_id, first_name="", last_name="Doe")
        assert exc.value.code == RegistrationError.INVALID_FIRST_NAME.code

    def test_invalid_last_name(self, valid_id):
        with pytest.raises(DomainException) as exc:
            Person(id=valid_id, first_name="Jane", last_name="")
        assert exc.value.code == RegistrationError.INVALID_LAST_NAME.code


class TestAcademy:
    def test_valid_creation(self, valid_id, valid_instructor):
        academy = Academy(id=valid_id, name="Miyagi-Do", instructor=valid_instructor)
        assert academy.name == "Miyagi-Do"
        assert academy.instructor == valid_instructor

    def test_invalid_name(self, valid_id, valid_instructor):
        with pytest.raises(DomainException) as exc:
            Academy(id=valid_id, name="", instructor=valid_instructor)
        assert exc.value.code == RegistrationError.INVALID_ACADEMY_NAME.code

    def test_invalid_instructor(self, valid_id):
        with pytest.raises(DomainException) as exc:
            Academy(id=valid_id, name="Miyagi-Do", instructor=None)  # type: ignore
        assert exc.value.code == RegistrationError.INVALID_ACADEMY_INSTRUCTOR.code


class TestRank:
    def test_valid_creation(self, valid_id):
        rank = Rank(id=valid_id, name="White Belt", is_black_belt=False)
        assert rank.name == "White Belt"
        assert rank.is_black_belt is False

    def test_invalid_name(self, valid_id):
        with pytest.raises(DomainException) as exc:
            Rank(id=valid_id, name="", is_black_belt=False)
        assert exc.value.code == RegistrationError.INVALID_RANK_NAME.code


class TestCompetitor:
    def test_valid_creation(self, valid_id, valid_academy, valid_rank, valid_sex):
        competitor = Competitor(
            id=valid_id,
            first_name="Daniel",
            last_name="LaRusso",
            academy=valid_academy,
            rank=valid_rank,
            sex=valid_sex,
            weight=70.5,
            height=175.0,
            special_condition=False,
        )
        assert competitor.full_name == "Daniel LaRusso"
        assert competitor.weight == 70.5

    def test_inheritance_validation(
        self, valid_id, valid_academy, valid_rank, valid_sex
    ):
        # Should fail due to Person validation (empty first name)
        with pytest.raises(DomainException) as exc:
            Competitor(
                id=valid_id,
                first_name="",
                last_name="LaRusso",
                academy=valid_academy,
                rank=valid_rank,
                sex=valid_sex,
                weight=70.5,
                height=175.0,
                special_condition=False,
            )
        assert exc.value.code == RegistrationError.INVALID_FIRST_NAME.code

    @pytest.mark.parametrize("invalid_weight", [0, -10.5])
    def test_invalid_weight(
        self, valid_id, valid_academy, valid_rank, valid_sex, invalid_weight
    ):
        with pytest.raises(DomainException) as exc:
            Competitor(
                id=valid_id,
                first_name="Daniel",
                last_name="LaRusso",
                academy=valid_academy,
                rank=valid_rank,
                sex=valid_sex,
                weight=invalid_weight,
                height=175.0,
                special_condition=False,
            )
        assert exc.value.code == RegistrationError.INVALID_WEIGHT.code

    @pytest.mark.parametrize("invalid_height", [0, -180.0])
    def test_invalid_height(
        self, valid_id, valid_academy, valid_rank, valid_sex, invalid_height
    ):
        with pytest.raises(DomainException) as exc:
            Competitor(
                id=valid_id,
                first_name="Daniel",
                last_name="LaRusso",
                academy=valid_academy,
                rank=valid_rank,
                sex=valid_sex,
                weight=70.5,
                height=invalid_height,
                special_condition=False,
            )
        assert exc.value.code == RegistrationError.INVALID_HEIGHT.code
