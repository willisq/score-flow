from math import ceil, log2
from uuid import UUID
from typing import Callable
from uuid import uuid4
from abc import ABC, abstractmethod
from typing import List

from src.features.registration.domain.entities import Competitor
from src.features.bracket.domain.entities import Match, Round


class PairingStrategy(ABC):
    """Abstract Strategy for pairing competitors."""

    @abstractmethod
    def pair(
        self,
        competitors: List[Competitor],
        current_round: Round,
        id_factory: Callable[[], UUID] = uuid4,
    ) -> List[Match]:
        """
        Pairs competitors for a round.

        Args:
            competitors: List of competitors to pair
            round: The round for which to create matches

        Returns:
            List of matches to be played in this round (including byes)
        """
        ...

    def _get_number_of_matches(self, number_of_competitors: int) -> int:
        """Returns the number of matches needed to pair all competitors."""
        return (
            2 ** (ceil(log2(number_of_competitors)) - 1)
            if number_of_competitors > 1
            else 1
        )


class AcademyAwarePairingStrategy(PairingStrategy):
    """Pairing strategy that takes into account the academy of the competitors."""

    def _find_second_competitor(
        self, first_competitor: Competitor, competitors: List[Competitor]
    ) -> Competitor | None:
        """Looks for an opponent from a different academy, or takes the next one if none found."""
        second_competitor = None

        # Look for an opponent from a different academy
        for i, candidate in enumerate(competitors):
            if candidate.academy.id != first_competitor.academy.id:
                second_competitor = competitors.pop(i)
                break

        # If no opponent from another academy is found, take the next one
        if second_competitor is None and competitors:
            second_competitor = competitors.pop(0)

        return second_competitor

    def pair(
        self,
        competitors: List[Competitor],
        current_round: Round,
        id_factory: Callable[[], UUID] = uuid4,
    ) -> List[Match]:
        """
        Pairs competitors according to business rules:
        1. Number of matches is a power of 2 (2^(ceil(log2(N))-1)).
        2. Byes are matches with one competitor and an automatic winner.
        3. Real matches avoid same-academy pairings where possible.
        """
        if not competitors:
            return []

        number_of_competitors = len(competitors)
        number_of_matches = self._get_number_of_matches(number_of_competitors)

        number_of_real_matches = number_of_competitors - number_of_matches
        number_of_byes = number_of_matches - number_of_real_matches

        matches = []

        # Create bye matches
        for index in range(number_of_byes):
            if not competitors:
                break
            competitor = competitors.pop(0)
            match = Match(
                id=id_factory(),
                round=current_round,
                first_competitor=competitor,
                second_competitor=None,
                position=index,
            )
            match.set_winner(competitor)
            matches.append(match)

        # Create real matches
        current_position = number_of_byes
        while competitors:
            first_competitor = competitors.pop(0)
            second_competitor = self._find_second_competitor(
                first_competitor, competitors
            )

            match = Match(
                id=id_factory(),
                round=current_round,
                first_competitor=first_competitor,
                second_competitor=second_competitor,
                position=current_position,
            )
            matches.append(match)
            current_position += 1

        return matches
