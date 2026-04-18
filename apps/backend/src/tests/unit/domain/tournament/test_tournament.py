import pytest
from src.core.common.exceptions import DomainException
from src.features.tournament.domain.entities import (
    Modality,
    Tournament,
    Category,
    CategoryModality,
    PhysicalRequirement,
)
from src.features.tournament.domain.errors import TournamentError


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


class TestPhysicalRequirement:
    def test_invalid_weight_limits(self, valid_id):
        with pytest.raises(DomainException) as exc:
            PhysicalRequirement(
                id=valid_id,
                initial_weight=-1,
                final_weight=70.0,
            )
        assert exc.value.code == TournamentError.INVALID_WEIGHT_LIMITS.code

    def test_invalid_weight_range(self, valid_id):
        with pytest.raises(DomainException) as exc:
            PhysicalRequirement(
                id=valid_id,
                initial_weight=70.0,
                final_weight=60.0,  # Initial > Final
            )
        assert exc.value.code == TournamentError.INVALID_WEIGHT_RANGE.code

    def test_invalid_height_limits(self, valid_id):
        with pytest.raises(DomainException) as exc:
            PhysicalRequirement(
                id=valid_id,
                initial_height=-1,
                final_height=175.0,
            )
        assert exc.value.code == TournamentError.INVALID_HEIGHT_LIMITS.code

    def test_invalid_height_range(self, valid_id):
        with pytest.raises(DomainException) as exc:
            PhysicalRequirement(
                id=valid_id,
                initial_height=175.0,
                final_height=165.0,
            )
        assert exc.value.code == TournamentError.INVALID_HEIGHT_RANGE.code


class TestCategory:
    def test_valid_creation(self, valid_id, valid_sex, valid_rank):
        category = Category(
            id=valid_id,
            ages=[18, 35],
            special_condition=False,
        )
        assert category.ages == [18, 35]

    @pytest.mark.parametrize("age", [-1, 0])
    def test_invalid_age_limits(
        self, valid_id, valid_sex, valid_rank, age
    ):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                ages=[age],
                special_condition=False,
            )
        assert exc.value.code == TournamentError.INVALID_AGE_LIMITS.code

    def test_invalid_age_list(self, valid_id, valid_sex, valid_rank):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                ages=[],
                special_condition=False,
            )
        assert exc.value.code == TournamentError.INVALID_AGE_LIST.code


class TestCategoryModality:
    def test_valid_creation(self, valid_id, valid_modality, valid_sex):
        # Create a base category
        category = Category(
            id=valid_id,
            ages=[18, 35],
            special_condition=False,
        )
        
        cat_mod = CategoryModality(
            id=valid_id,
            category=category,
            modality=valid_modality,
            sexes=[valid_sex],
        )
        assert cat_mod.category == category
        assert cat_mod.modality == valid_modality
