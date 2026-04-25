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

    def _interleave_competitors(self, competitors: List[Competitor]) -> List[Competitor]:
        """Groups competitors by academy and interleaves them to avoid consecutive teammates, with randomization."""
        import random
        from collections import defaultdict, deque

        # 1. Randomize the input list to ensure random assignment within academies
        shuffled_competitors = list(competitors)
        random.shuffle(shuffled_competitors)

        academy_groups = defaultdict(deque)
        for c in shuffled_competitors:
            academy_groups[c.academy.id].append(c)

        # 2. Sort groups by size descending, but randomize order within groups of the same size
        # We use a tuple (size, random_val) to sort
        sorted_keys = sorted(
            academy_groups.keys(),
            key=lambda k: (len(academy_groups[k]), random.random()),
            reverse=True,
        )
        ordered_groups = [academy_groups[k] for k in sorted_keys]

        interleaved = []
        while any(ordered_groups):
            for group in ordered_groups:
                if group:
                    interleaved.append(group.popleft())
        return interleaved

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
        4. Minimizes early round collisions using a greedy collision-aware slot assignment.
        """
        if not competitors:
            return []

        number_of_competitors = len(competitors)
        number_of_matches = self._get_number_of_matches(number_of_competitors)

        # 1. Prepare ordered list of competitors (use a copy to avoid mutating original list)
        ordered_competitors = self._interleave_competitors(list(competitors))

        # 2. Determine slot order (Match Index, Is First Slot)
        # We fill 'first' slots in bit-reversed order, then 'second' slots in reversed bit-reversed order.
        # This keeps teammates assigned to the same match at the maximum possible distance in the tree.
        match_order = self._get_bit_reversal_order(number_of_matches)

        slot_order = []
        for m_idx in match_order:
            slot_order.append((m_idx, True))
        for m_idx in reversed(match_order):
            slot_order.append((m_idx, False))

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

        # 4. Fill slots greedily avoiding collisions
        filled_slots = set()

        for competitor in ordered_competitors:
            chosen_slot_idx = -1
            fallback_slot_idx = -1

            for i, (m_idx, is_first) in enumerate(slot_order):
                if i in filled_slots:
                    continue

                if fallback_slot_idx == -1:
                    fallback_slot_idx = i  # Store the first available slot as fallback

                # Check for collision in this match
                match = matches_dict[m_idx]
                opponent = match.second_competitor if is_first else match.first_competitor
                
                if opponent is not None and opponent.academy.id == competitor.academy.id:
                    continue  # Causes collision, try next available slot

                chosen_slot_idx = i
                break

            if chosen_slot_idx == -1:
                # Unavoidable collision (pigeonhole principle), use the first available slot
                chosen_slot_idx = fallback_slot_idx

            filled_slots.add(chosen_slot_idx)
            m_idx, is_first = slot_order[chosen_slot_idx]
            match = matches_dict[m_idx]

            if is_first:
                match.first_competitor = competitor
            else:
                match.second_competitor = competitor

        # 5. Finalize and handle Byes
        final_matches = []
        for i in range(number_of_matches):
            match = matches_dict[i]

            # If a match only has one competitor, it's a bye
            if match.first_competitor is None and match.second_competitor is not None:
                # Swap to first if only second exists
                match.first_competitor = match.second_competitor
                match.second_competitor = None

            if match.second_competitor is None and match.first_competitor is not None:
                match.set_winner(match.first_competitor)

            final_matches.append(match)

        return final_matches
