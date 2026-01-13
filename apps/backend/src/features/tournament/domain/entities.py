from dataclasses import dataclass
from uuid import UUID
from typing import List
from src.core.common.exceptions import DomainException
from src.features.registration.domain.entities import Competitor, Rank, Sex
from src.features.tournament.domain.errors import TournamentError


@dataclass
class Modality:
    """Value Object representing the modality of a tournament."""

    id: UUID
    name: str

    def __post_init__(self):
        if not self.name:
            raise DomainException(
                TournamentError.INVALID_MODALITY_NAME.message,
                code=TournamentError.INVALID_MODALITY_NAME.code,
            )


@dataclass
class Tournament:
    """Aggregate root for the tournament."""

    id: UUID
    description: str

    def __post_init__(self):
        if not self.description:
            raise DomainException(
                TournamentError.INVALID_TOURNAMENT_DESCRIPTION.message,
                code=TournamentError.INVALID_TOURNAMENT_DESCRIPTION.code,
            )


@dataclass
class Category:
    """Entity defining a competition category."""

    id: UUID
    name: str
    initial_age: int
    final_age: int
    special_condition: bool
    modality: Modality
    sexes: List[Sex]
    ranks: List[Rank]
    initial_weight: float = None
    final_weight: float = None

    def __post_init__(self):
        if not self.name:
            raise DomainException(
                TournamentError.INVALID_CATEGORY_NAME.message,
                code=TournamentError.INVALID_CATEGORY_NAME.code,
            )
        if not self.modality:
            raise DomainException(
                TournamentError.INVALID_CATEGORY_MODALITY.message,
                code=TournamentError.INVALID_CATEGORY_MODALITY.code,
            )
        if self.initial_age < 0 or self.final_age < 0:
            raise DomainException(
                TournamentError.INVALID_AGE_LIMITS.message,
                code=TournamentError.INVALID_AGE_LIMITS.code,
            )
        if self.initial_age > self.final_age:
            raise DomainException(
                TournamentError.INVALID_AGE_RANGE.message,
                code=TournamentError.INVALID_AGE_RANGE.code,
            )


@dataclass
class CategoryRegistration:
    """Entity representing the registration of a competitor in a category."""

    id: UUID
    competitor: Competitor
    category: Category
    tournament: Tournament
