import pytest
from uuid import uuid4
from src.features.tournament.domain.entities import (
    Category,
    Modality,
    CategoryModality,
    PhysicalRequirement,
    RankGroup,
)
from src.features.registration.domain.entities import Competitor, Sex, Rank, Person, Academy


@pytest.fixture
def base_sex():
    return Sex(id=uuid4(), name="Male")


@pytest.fixture
def base_sex_f():
    return Sex(id=uuid4(), name="Female")


@pytest.fixture
def base_rank():
    return Rank(id=uuid4(), name="White Belt", classification=1, is_black_belt=False)


@pytest.fixture
def base_rank_2():
    return Rank(id=uuid4(), name="Blue Belt", classification=2, is_black_belt=False)


@pytest.fixture
def base_modality():
    return Modality(id=uuid4(), name="Kumite")


@pytest.fixture
def base_academy():
    person = Person(id=uuid4(), first_name="John", last_name="Doe")
    return Academy(id=uuid4(), name="Cobra Kai", instructor=person)


@pytest.fixture
def valid_competitor(base_academy, base_rank, base_sex):
    return Competitor(
        id=uuid4(),
        first_name="Daniel",
        last_name="LaRusso",
        academy=base_academy,
        rank=base_rank,
        sex=base_sex,
        age=18,
        weight=65.0,
        height=170.0,
        special_condition=False,
    )


@pytest.fixture
def base_category_modality(base_modality, base_sex, base_rank):
    category = Category(
        id=uuid4(), ages=[17, 18, 19], special_condition=False, sexes=[base_sex]
    )
    phys_req = PhysicalRequirement(
        id=uuid4(),
        initial_weight=60.0,
        final_weight=70.0,
        initial_height=160.0,
        final_height=180.0,
    )
    rank_group = RankGroup(id=uuid4(), name="Grup: Test", ranks=[base_rank])
    cat_mod = CategoryModality(
        id=uuid4(),
        category=category,
        modality=base_modality,
        rank_group=rank_group,
        physical_requirement=phys_req,
    )
    category.modalities.append(cat_mod)
    return cat_mod


def test_is_eligible_success(base_category_modality, valid_competitor):
    # Todo cumple
    assert base_category_modality.is_eligible(valid_competitor) is True


def test_is_eligible_fails_age(base_category_modality, valid_competitor):
    valid_competitor.age = 25
    assert base_category_modality.is_eligible(valid_competitor) is False


def test_is_eligible_fails_sex(base_category_modality, valid_competitor, base_sex_f):
    valid_competitor.sex = base_sex_f
    assert base_category_modality.is_eligible(valid_competitor) is False


def test_is_eligible_fails_rank(base_category_modality, valid_competitor, base_rank_2):
    valid_competitor.rank = base_rank_2
    assert base_category_modality.is_eligible(valid_competitor) is False


def test_is_eligible_fails_weight(base_category_modality, valid_competitor):
    valid_competitor.weight = 80.0
    assert base_category_modality.is_eligible(valid_competitor) is False


def test_is_eligible_fails_height(base_category_modality, valid_competitor):
    valid_competitor.height = 190.0
    assert base_category_modality.is_eligible(valid_competitor) is False


def test_is_eligible_fails_special_condition(base_category_modality, valid_competitor):
    valid_competitor.special_condition = True
    assert base_category_modality.is_eligible(valid_competitor) is False


def test_is_eligible_success_special_condition(base_category_modality, valid_competitor):
    base_category_modality.category.special_condition = True
    valid_competitor.special_condition = True
    assert base_category_modality.is_eligible(valid_competitor) is True
