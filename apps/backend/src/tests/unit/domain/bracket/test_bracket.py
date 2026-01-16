import pytest
from uuid import uuid4
from src.core.common.exceptions import DomainException
from src.features.bracket.domain.entities import Pyramid, Round, Match
from src.features.bracket.domain.errors import BracketError
from src.features.bracket.domain.pairing_strategies import AcademyAwarePairingStrategy
from src.features.registration.domain.entities import (
    Competitor,
)


@pytest.fixture
def academy_aware_strategy():
    return AcademyAwarePairingStrategy()


class TestRound:
    def test_valid_creation(self, valid_id):
        round_entity = Round(id=valid_id, description="Semi-Finals")
        assert round_entity.description == "Semi-Finals"

    def test_invalid_description(self, valid_id):
        with pytest.raises(DomainException) as exc:
            Round(id=valid_id, description="")
        assert exc.value.code == BracketError.INVALID_ROUND_DESCRIPTION.code


class TestMatch:
    def test_valid_creation(self, valid_id, valid_round, valid_competitor):
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

    def test_set_winner_invalid_competitor(
        self, valid_id, valid_round, valid_competitor
    ):
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

        # Trying to set a winner that is not part of the match
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


class TestPyramid:
    def test_generate_initial_round_with_even_competitors(
        self,
        valid_id,
        valid_category,
        valid_academy,
        valid_sex,
        valid_rank,
        academy_aware_strategy,
    ):
        # 1. Arrange
        # Creamos objetos falsos (mocks/stubs) para la prueba
        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"Competitor{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=valid_category.initial_weight,
                height=valid_category.initial_height,
                special_condition=False,
            )
            for i in range(8)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)

        # 2. Act (Actuar)
        matches = pyramid.generate_initial_round(competitors, academy_aware_strategy)

        # 3. Assert (Verificar)
        # La primera ronda para 8 competidores debe tener 4 partidos.
        assert len(pyramid.matches) == 4
        # Return value should be the same list
        assert matches == pyramid.matches

        # Verificamos que todos los competidores estén en algún partido.
        all_competitor_ids_in_matches = set()
        for match in pyramid.matches:
            all_competitor_ids_in_matches.add(match.first_competitor.id)
            if match.second_competitor:
                all_competitor_ids_in_matches.add(match.second_competitor.id)

        assert len(all_competitor_ids_in_matches) == 8

    def test_generate_initial_round_with_odd_competitors(
        self,
        valid_id,
        valid_category,
        valid_academy,
        valid_sex,
        valid_rank,
        academy_aware_strategy,
    ):
        # 1. Arrange - 5 competidores (número impar)
        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"Competitor{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=valid_category.initial_weight,
                height=valid_category.initial_height,
                special_condition=False,
            )
            for i in range(5)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)

        # 2. Act
        matches = pyramid.generate_initial_round(competitors, academy_aware_strategy)

        # 3. Assert
        # Con 5 competidores: 2 matches reales + 1 bye = 3 matches totales
        assert len(pyramid.matches) == 3
        assert matches == pyramid.matches

        # Identificar matches reales y byes
        real_matches = [m for m in matches if m.second_competitor is not None]
        bye_matches = [m for m in matches if m.second_competitor is None]

        assert len(real_matches) == 2
        assert len(bye_matches) == 1

        # Verificar ids únicos
        played_ids = set()
        for match in matches:
            played_ids.add(match.first_competitor.id)
            if match.second_competitor:
                played_ids.add(match.second_competitor.id)

        # 5 competidores en total
        assert len(played_ids) == 5
