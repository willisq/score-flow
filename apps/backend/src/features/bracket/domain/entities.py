from typing import Callable, TYPE_CHECKING
from uuid import uuid4
from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID
from src.core.common.exceptions import DomainException
from src.features.registration.domain.entities import Competitor
from src.features.tournament.domain.entities import Category
from src.features.bracket.domain.errors import BracketError

if TYPE_CHECKING:
    from src.features.bracket.domain.pairing_strategies import PairingStrategy


@dataclass
class Round:
    """Aggregate root for the match"""

    id: UUID
    description: str
    sequence: int = 1

    def __post_init__(self):
        if not self.description:
            raise DomainException(
                BracketError.INVALID_ROUND_DESCRIPTION.message,
                code=BracketError.INVALID_ROUND_DESCRIPTION.code,
            )


@dataclass
class Match:
    """Entity representing a match in a bracket."""

    id: UUID
    round: Round
    first_competitor: Competitor
    second_competitor: Optional[Competitor] = None
    position: int = 0
    winner: Optional[Competitor] = None

    def set_winner(self, competitor: Competitor) -> None:
        if competitor not in [self.first_competitor, self.second_competitor]:
            raise DomainException(
                BracketError.INVALID_MATCH_WINNER.message,
                code=BracketError.INVALID_MATCH_WINNER.code,
            )
        self.winner = competitor


@dataclass
class Pyramid:
    """Aggregate root for the tournament bracket."""

    id: UUID
    category: Category
    matches: List[Match] = field(default_factory=list)

    def generate_initial_round(
        self,
        competitors: List[Competitor],
        first_round: Round,
        pairing_strategy: "PairingStrategy",
        id_factory: Callable[[], UUID] = uuid4,
    ) -> List[Match]:
        """
        Generates the initial round of pairings using a strategy.

        Args:
            competitors: List of competitors to pair
            pairing_strategy: Pairing strategy to use
            id_factory: Function to generate UUIDs (injectable for tests)

        Returns:
            List of matches in the first round (including byes)
        """
        self.matches.clear()

        matches = pairing_strategy.pair(competitors, first_round, id_factory)

        self.matches.extend(matches)

        return matches

    def get_matches_by_round(self, round: Round) -> List[Match]:
        """Returns matches belonging to a specific round, sorted by position."""

        round_matches = [match for match in self.matches if match.round.id == round.id]
        return sorted(round_matches, key=lambda match: match.position)

    def is_round_complete(self, round: Round) -> bool:
        """Checks if all matches in a round have a winner."""

        round_matches = self.get_matches_by_round(round)
        if not round_matches:
            return False

        return all(match.winner is not None for match in round_matches)

    def get_round_winners(self, round: Round) -> List[Competitor]:
        """Returns the winners of a round in order of match position."""

        if not self.is_round_complete(round):
            raise DomainException(
                BracketError.ROUND_NOT_COMPLETE.message,
                code=BracketError.ROUND_NOT_COMPLETE.code,
            )
        round_matches = self.get_matches_by_round(round)
        return [m.winner for m in round_matches if m.winner is not None]

    def advance(
        self,
        current_round: Round,
        next_round: Round,
        pairing_strategy: "PairingStrategy",
        id_factory: Callable[[], UUID] = uuid4,
    ) -> List[Match]:
        """
        Advances the winners of the current round to the next round.
        """
        winners = self.get_round_winners(current_round)

        next_matches = pairing_strategy.pair(winners, next_round, id_factory)

        self.matches.extend(next_matches)
        return next_matches
