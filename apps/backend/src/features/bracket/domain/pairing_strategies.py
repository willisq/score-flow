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
    """
    Pairing strategy that takes into account the academy of the competitors
    and distributes them to maximize tree distance between teammates.
    """

    def _get_bit_reversal_order(self, n: int) -> List[int]:
        """Returns indices 0..n-1 in bit-reversed order."""
        if n <= 1:
            return [0]
        width = (n - 1).bit_length()
        return [int(f"{i:0{width}b}"[::-1], 2) for i in range(n)]

    def pair(
        self,
        competitors: List[Competitor],
        current_round: Round,
        id_factory: Callable[[], UUID] = uuid4,
    ) -> List[Match]:
        """
        Pairs competitors according to business rules:
        1. Number of matches is a power of 2 (2^(ceil(log2(N))-1)).
        2. Competitors from the same academy are distributed to different branches.
        3. Byes are distributed throughout the bracket.
        4. Prioritizes larger academies to maximize distance and avoid collisions.
        """
        if not competitors:
            return []

        import random
        from collections import defaultdict

        number_of_competitors = len(competitors)
        number_of_matches = self._get_number_of_matches(number_of_competitors)
        match_order = self._get_bit_reversal_order(number_of_matches)

        # 1. Group by academy and shuffle
        academy_groups = defaultdict(list)
        for c in competitors:
            academy_groups[c.academy.id].append(c)

        # 2. Sort academies by size descending, randomize order within same size
        sorted_academy_ids = sorted(
            academy_groups.keys(),
            key=lambda k: (len(academy_groups[k]), random.random()),
            reverse=True,
        )

        # 3. Create match shells
        matches_dict = {
            i: Match(
                id=id_factory(),
                round=current_round,
                first_competitor=None,  # type: ignore
                second_competitor=None,
                position=i,
            )
            for i in range(number_of_matches)
        }

        # 4. Place competitors academy by academy (Phase-based Greedy)
        for academy_id in sorted_academy_ids:
            teammates = academy_groups[academy_id]
            random.shuffle(teammates)

            for competitor in teammates:
                placed = False

                # Phase 1: Place in an EMPTY match (following bit-reversal order)
                for m_idx in match_order:
                    match = matches_dict[m_idx]
                    if match.first_competitor is None and match.second_competitor is None:
                        match.first_competitor = competitor
                        placed = True
                        break

                if placed:
                    continue

                # Phase 2: Place in a HALF-FULL match (no teammate)
                for m_idx in match_order:
                    match = matches_dict[m_idx]
                    if match.second_competitor is None:
                        # Since we fill sequentially, first_competitor is guaranteed not None here
                        if match.first_competitor.academy.id != academy_id:
                            match.second_competitor = competitor
                            placed = True
                            break

                if placed:
                    continue

                # Phase 3: Unavoidable collision (Pigeonhole principle)
                for m_idx in match_order:
                    match = matches_dict[m_idx]
                    if match.second_competitor is None:
                        match.second_competitor = competitor
                        placed = True
                        break

        # 5. Finalize and handle Byes
        final_matches = []
        for i in range(number_of_matches):
            match = matches_dict[i]

            # Ensure first slot is always filled if there's only one competitor
            if match.first_competitor is None and match.second_competitor is not None:
                match.first_competitor = match.second_competitor
                match.second_competitor = None

            if match.second_competitor is None and match.first_competitor is not None:
                match.set_winner(match.first_competitor)

            final_matches.append(match)

        return final_matches
