from typing import Callable
from pytest import fixture
from uuid import UUID, uuid4
from src.features.registration.domain.entities import (
    Competitor,
    Academy,
    Person,
    Rank,
    Sex,
)
from src.features.tournament.domain.entities import Category, Modality
from src.features.bracket.domain.entities import Round


@fixture
def valid_id() -> Callable[[], UUID]:
    return lambda: uuid4()


@fixture
def valid_rank(valid_id) -> Rank:
    return Rank(id=valid_id(), name="White", classification=1, is_black_belt=False)


@fixture
def valid_sex(valid_id) -> Sex:
    return Sex(id=valid_id(), name="Male")


@fixture
def valid_person(valid_id) -> Person:
    return Person(id=valid_id(), first_name="John", last_name="Doe")


@fixture
def valid_academy(valid_id, valid_person) -> Academy:
    return Academy(id=valid_id(), name="Dojo", instructor=valid_person)


@fixture
def valid_competitor(valid_id, valid_academy, valid_rank, valid_sex) -> Competitor:
    return Competitor(
        id=valid_id(),
        first_name="John",
        last_name="Doe",
        academy=valid_academy,
        rank=valid_rank,
        sex=valid_sex,
        weight=70.0,
        height=170.0,
        special_condition=False,
    )


@fixture
def valid_round(valid_id) -> Round:
    return Round(id=valid_id(), description="Finals")


@fixture
def valid_modality(valid_id) -> Modality:
    return Modality(id=valid_id(), name="Sparring")


@fixture
def valid_category(valid_id, valid_modality, valid_sex, valid_rank) -> Category:
    return Category(
        id=valid_id(),
        special_condition=False,
        sexes=[valid_sex],
        ages=[18, 35],
    )
