import pytest
from src.core.common.exceptions import DomainException
from src.features.tournament.domain.entities import (
    Modality,
    Tournament,
    Category,
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


class TestCategory:
    def test_valid_creation(self, valid_id, valid_modality, valid_sex, valid_rank):
        category = Category(
            id=valid_id,
            name="Elite Male -70kg",
            ages=[18, 35],
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
                special_condition=False,
                modality=valid_modality,
                sexes=[valid_sex],
                ranks=[valid_rank],
                ages=[18, 35],
            )
        assert exc.value.code == TournamentError.INVALID_CATEGORY_NAME.code

    def test_invalid_modality(self, valid_id, valid_sex, valid_rank):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                name="Test Category",
                special_condition=False,
                modality=None,  # type: ignore
                sexes=[valid_sex],
                ranks=[valid_rank],
                ages=[18, 35],
            )
        assert exc.value.code == TournamentError.INVALID_CATEGORY_MODALITY.code

    @pytest.mark.parametrize("age", [-1, 0])
    def test_invalid_age_limits(
        self, valid_id, valid_modality, valid_sex, valid_rank, age
    ):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                name="Test",
                ages=[age],
                special_condition=False,
                modality=valid_modality,
                sexes=[valid_sex],
                ranks=[valid_rank],
            )
        assert exc.value.code == TournamentError.INVALID_AGE_LIMITS.code

    def test_invalid_weight_limits(
        self, valid_id, valid_modality, valid_sex, valid_rank
    ):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                name="Test",
                ages=[1, 70],
                special_condition=False,
                modality=valid_modality,
                sexes=[valid_sex],
                ranks=[valid_rank],
                initial_weight=-1,
                final_weight=70.0,
            )
        assert exc.value.code == TournamentError.INVALID_WEIGHT_LIMITS.code

    def test_invalid_weight_range(
        self, valid_id, valid_modality, valid_sex, valid_rank
    ):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                name="Test",
                ages=[1, 70],
                special_condition=False,
                modality=valid_modality,
                sexes=[valid_sex],
                ranks=[valid_rank],
                initial_weight=70.0,
                final_weight=60.0,  # Initial > Final
            )
        assert exc.value.code == TournamentError.INVALID_WEIGHT_RANGE.code

    def test_invalid_height_limits(
        self, valid_id, valid_modality, valid_sex, valid_rank
    ):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                name="Test",
                ages=[1, 70],
                special_condition=False,
                modality=valid_modality,
                sexes=[valid_sex],
                ranks=[valid_rank],
                initial_height=-1,
                final_height=175.0,
            )
        assert exc.value.code == TournamentError.INVALID_HEIGHT_LIMITS.code

    def test_invalid_height_range(
        self, valid_id, valid_modality, valid_sex, valid_rank
    ):
        with pytest.raises(DomainException) as exc:
            Category(
                id=valid_id,
                name="Test",
                ages=[1, 70],
                special_condition=False,
                modality=valid_modality,
                sexes=[valid_sex],
                ranks=[valid_rank],
                initial_height=175.0,
                final_height=165.0,
            )
        assert exc.value.code == TournamentError.INVALID_HEIGHT_RANGE.code
