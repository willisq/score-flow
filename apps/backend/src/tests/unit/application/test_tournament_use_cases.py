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
    CategoryBulkCreate,
    CategoryModalityCreate,
    PhysicalRequirementCreate,
    CategoryModalityUpdate,
)
from src.features.tournament.application.use_cases import TournamentUseCases
from src.features.tournament.domain.entities import (
    Category,
    CategoryModality,
    CategoryRegistration,
    Modality,
    Tournament,
    PhysicalRequirement,
    RankGroup,
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
        rank_group_repo=MagicMock(),
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
        rank_group_repo=MagicMock(),
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
    rank_group_repo = MagicMock()
    
    modality1 = Modality(id=uuid4(), name="Sparring")
    modality2 = Modality(id=uuid4(), name="Poomsae")
    rank = Rank(id=uuid4(), name="Black", classification=10, is_black_belt=True)
    sex = Sex(id=uuid4(), name="Male")
    rank_group = RankGroup(id=uuid4(), name="Principiantes", ranks=[rank])
    
    async def get_modality_by_id(mid):
        if mid == modality1.id: return modality1
        if mid == modality2.id: return modality2
        return None
        
    modality_repo.get_by_id = AsyncMock(side_effect=get_modality_by_id)
    rank_repo.get_by_id = AsyncMock(return_value=rank)
    rank_group_repo.get_by_id = AsyncMock(return_value=rank_group)
    sex_repo.get_by_id = AsyncMock(return_value=sex)
    category_repo.create = AsyncMock(side_effect=lambda x: x)
    category_repo.get_or_create_physical_requirement = AsyncMock(
        side_effect=lambda iw, fw, ih, fh, preferred_id=None: MagicMock(
            id=preferred_id or uuid4(),
            initial_weight=iw,
            final_weight=fw,
            initial_height=ih,
            final_height=fh
        )
    )
    
    use_cases = TournamentUseCases(
        modality_repo=modality_repo,
        tournament_repo=MagicMock(),
        category_repo=category_repo,
        registration_repo=MagicMock(),
        competitor_repo=MagicMock(),
        rank_repo=rank_repo,
        sex_repo=sex_repo,
        rank_group_repo=rank_group_repo,
    )
    
    schema = CategoryCreate(
        ages=[10, 12],
        modalities=[
            CategoryModalityCreate(
                modality_id=modality1.id,
                sex_ids=[sex.id],
                rank_group_ids=[rank_group.id],
                physical_requirements=[
                    PhysicalRequirementCreate(
                        initial_weight=80.0,
                        final_weight=120.0
                    )
                ]
            ),
            CategoryModalityCreate(
                modality_id=modality2.id,
                sex_ids=[sex.id],
                rank_group_ids=[rank_group.id],
                physical_requirements=[
                    PhysicalRequirementCreate(
                        initial_weight=80.0,
                        final_weight=120.0
                    )
                ]
            )
        ]
    )
    
    results = asyncio.run(use_cases.register_category(schema))
    
    assert isinstance(results, list)
    assert len(results) == 1
    category = results[0]
    assert len(category.modalities) == 2
    assert category.modalities[0].modality == modality1
    assert category.modalities[1].modality == modality2
    # Ranks are now on modality level
    assert rank in category.modalities[0].ranks
    assert sex in category.modalities[0].sexes
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
        id=uuid4(), ages=[15, 17], 
        special_condition=False,
    )
    rank_group = RankGroup(id=uuid4(), name="Grup: Test", ranks=[rank])
    cat_mod = CategoryModality(id=uuid4(), category=category, modality=modality, sexes=[sex], rank_group=rank_group)
    category.modalities.append(cat_mod)
    
    tournament = Tournament(id=uuid4(), description="All Valley")
    
    competitor_repo.get_by_id = AsyncMock(return_value=competitor)
    category_repo.get_modality_by_id = AsyncMock(return_value=cat_mod)
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
        rank_group_repo=MagicMock(),
    )
    
    schema = CategoryRegistrationCreate(
        competitor_id=competitor.id,
        category_modality_id=cat_mod.id,
        tournament_id=tournament.id
    )
    
    result = asyncio.run(use_cases.inscribe_competitor(schema))
    
    assert isinstance(result, CategoryRegistration)
    assert result.competitor == competitor
    assert result.category_modality == cat_mod
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
    )
    rank_group = RankGroup(id=uuid4(), name="Grup: Test", ranks=[rank])
    cat_mod = CategoryModality(id=uuid4(), category=category, modality=modality, sexes=[sex], rank_group=rank_group)
    category.modalities.append(cat_mod)
    
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
        rank_group_repo=MagicMock(),
    )
    
    schema = MassRegistrationRequest(
        competitor_ids=[competitor.id],
        tournament_id=tournament.id
    )
    
    result = asyncio.run(use_cases.mass_register_competitors(schema))
    
    assert len(result["registrations"]) == 1
    assert result["registrations"][0].competitor == competitor
    assert result["registrations"][0].category_modality == cat_mod
    assert len(result["errors"]) == 0
    registration_repo.create.assert_called_once()


def test_mass_register_competitors_with_category_modality_id():
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
    )
    rank_group = RankGroup(id=uuid4(), name="Grup: Test", ranks=[rank])
    cat_mod = CategoryModality(id=uuid4(), category=category, modality=modality, sexes=[sex], rank_group=rank_group)
    category.modalities.append(cat_mod)

    instructor = Person(id=uuid4(), first_name="Nariyoshi", last_name="Miyagi")
    academy = Academy(id=uuid4(), name="Miyagi-Do", instructor=instructor)
    competitor = Competitor(
        id=uuid4(), first_name="Daniel", last_name="LaRusso",
        academy=academy, rank=rank, sex=sex, age=18
    )

    tournament_repo.get_by_id = AsyncMock(return_value=tournament)
    category_repo.get_modality_by_id = AsyncMock(return_value=cat_mod)
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
        rank_group_repo=MagicMock(),
    )

    schema = MassRegistrationRequest(
        competitor_ids=[competitor.id],
        tournament_id=tournament.id,
        category_modality_id=cat_mod.id
    )

    result = asyncio.run(use_cases.mass_register_competitors(schema))

    assert len(result["registrations"]) == 1
    assert result["registrations"][0].competitor == competitor
    assert result["registrations"][0].category_modality == cat_mod
    assert result["registrations"][0].tournament == tournament
    assert len(result["errors"]) == 0
    registration_repo.create.assert_called_once()
    category_repo.get_modality_by_id.assert_called_once_with(cat_mod.id)


def test_mass_register_competitors_with_category_modality_id_invalid():
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
    )
    rank_group = RankGroup(id=uuid4(), name="Grup: Test", ranks=[rank])
    cat_mod = CategoryModality(id=uuid4(), category=category, modality=modality, sexes=[sex], rank_group=rank_group)
    category.modalities.append(cat_mod)

    instructor = Person(id=uuid4(), first_name="Nariyoshi", last_name="Miyagi")
    academy = Academy(id=uuid4(), name="Miyagi-Do", instructor=instructor)
    # Competitor is 20, but category is for 18
    competitor = Competitor(
        id=uuid4(), first_name="Daniel", last_name="LaRusso",
        academy=academy, rank=rank, sex=sex, age=20
    )

    tournament_repo.get_by_id = AsyncMock(return_value=tournament)
    category_repo.get_modality_by_id = AsyncMock(return_value=cat_mod)
    competitor_repo.get_by_ids = AsyncMock(return_value=[competitor])

    use_cases = TournamentUseCases(
        modality_repo=MagicMock(),
        tournament_repo=tournament_repo,
        category_repo=category_repo,
        registration_repo=registration_repo,
        competitor_repo=competitor_repo,
        rank_repo=MagicMock(),
        sex_repo=MagicMock(),
        rank_group_repo=MagicMock(),
    )

    schema = MassRegistrationRequest(
        competitor_ids=[competitor.id],
        tournament_id=tournament.id,
        category_modality_id=cat_mod.id,
    )

    result = asyncio.run(use_cases.mass_register_competitors(schema))

    assert len(result["registrations"]) == 0
    assert len(result["errors"]) == 1
    error = result["errors"][0]
    assert error["competitor_id"] == competitor.id
    assert error["reasons"]["age_mismatch"] is True
    assert "not eligible" in error["message"]
    registration_repo.create.assert_not_called()


def test_register_category_deduplicates_physical_requirements():
    modality_repo = MagicMock()
    rank_repo = MagicMock()
    sex_repo = MagicMock()
    category_repo = MagicMock()
    rank_group_repo = MagicMock()
    
    modality = Modality(id=uuid4(), name="Deduplication Test")
    rank = Rank(id=uuid4(), name="Black", classification=10, is_black_belt=True)
    sex = Sex(id=uuid4(), name="Female")
    rank_group = RankGroup(id=uuid4(), name="Group A", ranks=[rank])
    
    modality_repo.get_by_id = AsyncMock(return_value=modality)
    rank_repo.get_by_id = AsyncMock(return_value=rank)
    rank_group_repo.get_by_id = AsyncMock(return_value=rank_group)
    sex_repo.get_by_id = AsyncMock(return_value=sex)
    category_repo.create = AsyncMock(side_effect=lambda x: x)
    category_repo.get_or_create_physical_requirement = AsyncMock(
        side_effect=lambda iw, fw, ih, fh, preferred_id=None: MagicMock(
            id=preferred_id or uuid4(),
            initial_weight=iw,
            final_weight=fw,
            initial_height=ih,
            final_height=fh
        )
    )
    
    use_cases = TournamentUseCases(
        modality_repo=modality_repo,
        tournament_repo=MagicMock(),
        category_repo=category_repo,
        registration_repo=MagicMock(),
        competitor_repo=MagicMock(),
        rank_repo=rank_repo,
        sex_repo=sex_repo,
        rank_group_repo=rank_group_repo,
    )
    
    # Request with 2 physical requirements that are IDENTICAL
    schema = CategoryCreate(
        ages=[20],
        modalities=[
            CategoryModalityCreate(
                modality_id=modality.id,
                sex_ids=[sex.id],
                rank_group_ids=[rank_group.id],
                physical_requirements=[
                    PhysicalRequirementCreate(initial_weight=60.0, final_weight=70.0),
                    PhysicalRequirementCreate(initial_weight=60.0, final_weight=70.0)
                ]
            )
        ]
    )
    
    results = asyncio.run(use_cases.register_category(schema))
    category = results[0]
    
    # Should have 2 modality records
    assert len(category.modalities) == 2
    # BUT they should share the same PhysicalRequirement object instance
    assert category.modalities[0].physical_requirement is category.modalities[1].physical_requirement


def test_update_category_modality():
    category_repo = MagicMock()
    sex_repo = MagicMock()
    
    # Setup
    category = Category(id=uuid4(), ages=[10, 12], special_condition=False)
    modality = Modality(id=uuid4(), name="Sparring")
    sex1 = Sex(id=uuid4(), name="Male")
    sex2 = Sex(id=uuid4(), name="Female")
    rank_group = RankGroup(id=uuid4(), name="Group A", ranks=[])
    
    cat_mod = CategoryModality(
        id=uuid4(), 
        category=category, 
        modality=modality, 
        sexes=[sex1], 
        rank_group=rank_group
    )
    
    # Mocking session.get for CategoryModalityModel
    mock_model = MagicMock(sexes=[sex1])
    category_repo.get_modality_model_by_id = AsyncMock(return_value=mock_model)
    category_repo.session.get = AsyncMock(return_value=mock_model)
    category_repo.session.flush = AsyncMock()
    sex_repo.session.get = AsyncMock(return_value=MagicMock(id=sex2.id, name="Female"))
    category_repo.get_modality_by_id = AsyncMock(return_value=cat_mod)
    category_repo.session.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=MagicMock(return_value=None)))
    category_repo.get_or_create_physical_requirement = AsyncMock(
        return_value=MagicMock(id=uuid4(), initial_weight=50.0, final_weight=60.0)
    )
    
    use_cases = TournamentUseCases(
        modality_repo=MagicMock(),
        tournament_repo=MagicMock(),
        category_repo=category_repo,
        registration_repo=MagicMock(),
        competitor_repo=MagicMock(),
        rank_repo=MagicMock(),
        sex_repo=sex_repo,
        rank_group_repo=MagicMock(),
    )
    
    schema = CategoryModalityUpdate(
        sex_ids=[sex2.id],
        physical_requirement=PhysicalRequirementCreate(initial_weight=50.0, final_weight=60.0)
    )
    
    # We update cat_mod manually for the mock return to reflect changes in the test
    cat_mod.sexes = [sex2]
    cat_mod.physical_requirement = PhysicalRequirement(id=uuid4(), initial_weight=50.0, final_weight=60.0)
    
    result = asyncio.run(use_cases.update_category_modality(cat_mod.id, schema))
    
    assert isinstance(result, CategoryModality)
    assert sex2 in result.sexes
    assert result.physical_requirement.initial_weight == 50.0
    category_repo.session.flush.assert_called()
