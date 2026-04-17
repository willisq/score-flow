import pytest
from uuid import uuid4

from src.features.registration.domain.entities import Competitor, Sex, Rank, Person, Academy
from src.features.tournament.domain.entities import Category, Modality, Tournament, CategoryModality, PhysicalRequirement
from src.features.tournament.domain.services import AutoRegistrationService

@pytest.fixture
def base_sex():
    return Sex(id=uuid4(), name="Male")


@pytest.fixture
def base_rank():
    return Rank(id=uuid4(), name="White Belt", classification=1, is_black_belt=False)


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
        special_condition=False
    )

@pytest.fixture
def invalid_competitor(base_academy, base_rank, base_sex):
    return Competitor(
        id=uuid4(),
        first_name="Johnny",
        last_name="Lawrence",
        academy=base_academy,
        rank=base_rank,
        sex=base_sex,
        age=35, # Too old for the category
        weight=80.0,
        height=180.0,
        special_condition=False
    )


@pytest.fixture
def base_category(base_sex, base_rank):
    modality = Modality(id=uuid4(), name="Kumite")
    category = Category(
        id=uuid4(),
        ages=[17, 18, 19],
        special_condition=False,
        sexes=[base_sex],
        ranks=[base_rank]
    )
    phys_req = PhysicalRequirement(
        id=uuid4(),
        initial_weight=60.0,
        final_weight=70.0,
        initial_height=160.0,
        final_height=180.0
    )
    cat_mod = CategoryModality(
        id=uuid4(),
        category=category,
        modality=modality,
        physical_requirement=phys_req
    )
    category.modalities.append(cat_mod)
    return category


@pytest.fixture
def base_tournament():
    return Tournament(id=uuid4(), description="All Valley Tournament 1984")


def test_auto_register_competitors(valid_competitor, invalid_competitor, base_category, base_tournament):
    competitors = [valid_competitor, invalid_competitor]
    categories = [base_category]
    
    registrations = AutoRegistrationService.auto_register_competitors(
        competitors, categories, base_tournament
    )
    
    # Only valid_competitor matches base_category.modalities[0]
    assert len(registrations) == 1
    
    registration = registrations[0]
    assert registration.competitor.id == valid_competitor.id
    assert registration.category_modality.id == base_category.modalities[0].id
    assert registration.tournament.id == base_tournament.id
    assert registration.id is not None
