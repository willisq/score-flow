from dataclasses import dataclass, field
from typing import List, Optional
from uuid import UUID
from src.core.common.exceptions import DomainException
from src.features.registration.domain.entities import Competitor
from src.features.tournament.domain.entities import Category
from .errors import BracketError


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
    first_competitor: Optional[Competitor] = None
    second_competitor: Optional[Competitor] = None
    winner: Optional[Competitor] = None

    def set_winner(self, competitor: Competitor):
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
