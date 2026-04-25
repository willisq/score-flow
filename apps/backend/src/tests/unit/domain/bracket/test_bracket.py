import pytest
from uuid import uuid4
from src.core.common.exceptions import DomainException
from src.features.bracket.domain.entities import Pyramid, Round, Match
from src.features.bracket.domain.errors import BracketError
from src.features.bracket.domain.pairing_strategies import AcademyAwarePairingStrategy
from src.features.registration.domain.entities import (
    Competitor,
)

5


@pytest.fixture
def academy_aware_strategy():
    return AcademyAwarePairingStrategy()


class TestRound:
    def test_valid_creation(self, valid_id) -> None:
        round_entity = Round(id=valid_id, description="Semi-Finals")
        assert round_entity.description == "Semi-Finals"

    def test_invalid_description(self, valid_id) -> None:
        with pytest.raises(DomainException) as exc:
            Round(id=valid_id, description="")
        assert exc.value.code == BracketError.INVALID_ROUND_DESCRIPTION.code


class TestMatch:
    def test_valid_creation(self, valid_id, valid_round, valid_competitor) -> None:
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

    def test_set_winner_success(self, valid_id, valid_round, valid_competitor) -> None:
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
    ) -> None:
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
        valid_round,
        academy_aware_strategy,
    ) -> None:
        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"Competitor{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=60.0,
                height=170.0,
                special_condition=False,
            )
            for i in range(8)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)

        matches = pyramid.generate_initial_round(
            competitors, valid_round, academy_aware_strategy
        )

        assert len(pyramid.matches) == 4
        assert matches == pyramid.matches

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
        valid_round,
        academy_aware_strategy,
    ) -> None:
        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"Competitor{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=60.0,
                height=170.0,
                special_condition=False,
            )
            for i in range(5)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)

        matches = pyramid.generate_initial_round(
            competitors, valid_round, academy_aware_strategy
        )

        # With 5 competitors:
        # Nearest power of 2 is 8. Matches = 8/2 = 4.
        # Byes = 2*4 - 5 = 3.
        # Real matches = 5 - 4 = 1.
        assert len(pyramid.matches) == 4
        assert matches == pyramid.matches

        # All matches should be in the provided round
        for match in matches:
            assert match.round.description == valid_round.description

        # Identify real matches and bye matches
        real_matches = [m for m in matches if m.second_competitor is not None]
        bye_matches = [m for m in matches if m.second_competitor is None]

        assert len(real_matches) == 1
        assert len(bye_matches) == 3

        # Verify byes have winners
        for match in bye_matches:
            assert match.winner == match.first_competitor

        # Verify unique ids
        played_ids = set()
        for match in matches:
            played_ids.add(match.first_competitor.id)
            if match.second_competitor:
                played_ids.add(match.second_competitor.id)

        assert len(played_ids) == 5

    def test_generate_initial_round_with_ten_competitors(
        self,
        valid_id,
        valid_category,
        valid_academy,
        valid_sex,
        valid_rank,
        valid_round,
        academy_aware_strategy,
    ) -> None:
        # 1. Arrange - 10 competitors
        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"Competitor{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=60.0,
                height=170.0,
                special_condition=False,
            )
            for i in range(10)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)

        # 2. Act
        matches = pyramid.generate_initial_round(
            competitors, valid_round, academy_aware_strategy
        )

        # 3. Assert
        # With 10 competitors:
        # Nearest power of 2 is 16. Matches = 16/2 = 8.
        # Byes = 2*8 - 10 = 6.
        # Real matches = 10 - 8 = 2.
        assert len(pyramid.matches) == 8
        assert matches == pyramid.matches

        # All matches should be in the provided round
        for match in matches:
            assert match.round.description == valid_round.description

        # Identify real matches and bye matches
        real_matches = [m for m in matches if m.second_competitor is not None]
        bye_matches = [m for m in matches if m.second_competitor is None]

        assert len(real_matches) == 2
        assert len(bye_matches) == 6

        # Verify byes have winners
        for match in bye_matches:
            assert match.winner == match.first_competitor

        # Verify unique ids
        played_ids = set()
        for match in matches:
            played_ids.add(match.first_competitor.id)
            if match.second_competitor:
                played_ids.add(match.second_competitor.id)

        # 10 competitors in total
        assert len(played_ids) == 10

    def test_get_round_winners(
        self,
        valid_id,
        valid_round,
        valid_category,
        valid_academy,
        valid_sex,
        valid_rank,
        academy_aware_strategy,
    ) -> None:
        # Arrange
        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"C{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=60.0,
                height=170.0,
                special_condition=False,
            )
            for i in range(4)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)
        matches_r1 = pyramid.generate_initial_round(
            competitors, valid_round, academy_aware_strategy, valid_id
        )

        # Act 1: Set winners for R1
        for match in matches_r1:
            match.set_winner(match.first_competitor)

        # Act 2: Get winners for R1
        winners = pyramid.get_round_winners(valid_round)

        # Assert
        assert len(winners) == 2
        assert winners == [m.first_competitor for m in matches_r1]

    def test_get_matches_by_round(
        self,
        valid_id,
        valid_round,
        valid_category,
        valid_academy,
        valid_sex,
        valid_rank,
        academy_aware_strategy,
    ) -> None:
        # Arrange
        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"C{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=60.0,
                height=170.0,
                special_condition=False,
            )
            for i in range(4)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)
        matches_r1 = pyramid.generate_initial_round(
            competitors, valid_round, academy_aware_strategy, valid_id
        )

        # Act
        matches = pyramid.get_matches_by_round(valid_round)

        # Assert
        assert len(matches) == 2
        assert matches == matches_r1

    def test_advance_to_next_round(
        self,
        valid_id,
        valid_category,
        valid_academy,
        valid_sex,
        valid_rank,
        academy_aware_strategy,
    ) -> None:
        # Arrange
        round1 = Round(id=uuid4(), description="Round 1", sequence=1)
        round2 = Round(id=uuid4(), description="Round 2", sequence=2)

        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"C{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=60.0,
                height=170.0,
                special_condition=False,
            )
            for i in range(4)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)
        matches_r1 = pyramid.generate_initial_round(
            competitors, round1, academy_aware_strategy
        )

        # Act 1: Set winners for R1
        for match in matches_r1:
            match.set_winner(match.first_competitor)

        # Act 2: Advance to R2
        matches_r2 = pyramid.advance(round1, round2, academy_aware_strategy)

        # Assert
        assert len(matches_r2) == 1
        assert matches_r2[0].round.id == round2.id
        assert matches_r2[0].first_competitor == matches_r1[0].winner
        assert matches_r2[0].second_competitor == matches_r1[1].winner
        assert len(pyramid.matches) == 3  # 2 from R1 + 1 from R2

    def test_cannot_advance_if_round_incomplete(
        self,
        valid_id,
        valid_category,
        valid_academy,
        valid_sex,
        valid_rank,
        academy_aware_strategy,
    ) -> None:
        # Arrange
        round1 = Round(id=uuid4(), description="Round 1", sequence=1)
        round2 = Round(id=uuid4(), description="Round 2", sequence=2)

        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"C{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=60.0,
                height=170.0,
                special_condition=False,
            )
            for i in range(4)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)
        matches_r1 = pyramid.generate_initial_round(
            competitors, round1, academy_aware_strategy
        )

        # Only set winner for the first match
        matches_r1[0].set_winner(matches_r1[0].first_competitor)

        # Act & Assert
        with pytest.raises(DomainException) as exc:
            pyramid.advance(round1, round2, academy_aware_strategy)
        assert exc.value.code == BracketError.ROUND_NOT_COMPLETE.code

    def test_match_ordering_within_round(
        self,
        valid_id,
        valid_category,
        valid_academy,
        valid_sex,
        valid_rank,
        academy_aware_strategy,
    ) -> None:
        # Arrange
        round1 = Round(id=uuid4(), description="Round 1", sequence=1)
        competitors = [
            Competitor(
                id=uuid4(),
                academy=valid_academy,
                first_name=f"C{i}",
                last_name="Doe",
                rank=valid_rank,
                sex=valid_sex,
                weight=60.0,
                height=170.0,
                special_condition=False,
            )
            for i in range(4)
        ]

        pyramid = Pyramid(id=valid_id, category=valid_category)
        pyramid.generate_initial_round(competitors, round1, academy_aware_strategy)

        # Assert
        matches = pyramid.get_matches_by_round(round1)
        assert matches[0].position == 0
        assert matches[1].position == 1

    def test_academy_distribution_minimizes_early_collisions(
        self,
        valid_id,
        valid_category,
        valid_sex,
        valid_rank,
        valid_round,
        academy_aware_strategy,
    ) -> None:
        """
        Verify that teammates from the same academy are distributed across the bracket
        to avoid facing each other in early rounds.
        """
        from src.features.registration.domain.entities import Academy, Person

        # Arrange: 2 academies, 4 competitors each (total 8)
        academy_a = Academy(id=uuid4(), name="Academy A", instructor=Person(uuid4(), "I1", "L1"))
        academy_b = Academy(id=uuid4(), name="Academy B", instructor=Person(uuid4(), "I2", "L2"))

        competitors = []
        for i in range(4):
            competitors.append(Competitor(uuid4(), f"A{i}", "Doe", academy_a, valid_rank, valid_sex, 60.0, 170.0, 20, False))
            competitors.append(Competitor(uuid4(), f"B{i}", "Doe", academy_b, valid_rank, valid_sex, 60.0, 170.0, 20, False))

        pyramid = Pyramid(id=valid_id, category=valid_category)

        # Act
        matches = pyramid.generate_initial_round(competitors, valid_round, academy_aware_strategy)

        # Assert: 8 competitors -> 4 matches in 1st round
        assert len(matches) == 4

        # Verify no two teammates in the same match
        for match in matches:
            if match.first_competitor and match.second_competitor:
                assert match.first_competitor.academy.id != match.second_competitor.academy.id

        # Verify teammates are in different halves where possible
        # Semi-final 1: matches 0 & 1. Semi-final 2: matches 2 & 3.
        # Academy A members should be split 2 and 2 between halves.
        half1_matches = [m for m in matches if m.position < 2]
        half2_matches = [m for m in matches if m.position >= 2]

        def count_academy(matches_list, academy_id):
            count = 0
            for m in matches_list:
                if m.first_competitor and m.first_competitor.academy.id == academy_id:
                    count += 1
                if m.second_competitor and m.second_competitor.academy.id == academy_id:
                    count += 1
            return count

        assert count_academy(half1_matches, academy_a.id) == 2
        assert count_academy(half2_matches, academy_a.id) == 2
        assert count_academy(half1_matches, academy_b.id) == 2
        assert count_academy(half2_matches, academy_b.id) == 2
