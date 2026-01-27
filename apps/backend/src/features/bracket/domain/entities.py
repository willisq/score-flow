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
