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
    ages: List[int]
    special_condition: bool
    modality: Modality
    sexes: List[Sex]
    ranks: List[Rank]
    initial_weight: float = None
    final_weight: float = None
    initial_height: float = None
    final_height: float = None

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
        if len(self.ages) == 0:
            raise DomainException(
                TournamentError.INVALID_AGE_LIST.message,
                code=TournamentError.INVALID_AGE_LIST.code,
            )
        if any(age <= 0 for age in self.ages):
            raise DomainException(
                TournamentError.INVALID_AGE_LIMITS.message,
                code=TournamentError.INVALID_AGE_LIMITS.code,
            )
        if self._has_weight_limits and (
            self.initial_weight < 0 or self.final_weight < 0
        ):
            raise DomainException(
                TournamentError.INVALID_WEIGHT_LIMITS.message,
                code=TournamentError.INVALID_WEIGHT_LIMITS.code,
            )
        if self._has_weight_limits and self.initial_weight > self.final_weight:
            raise DomainException(
                TournamentError.INVALID_WEIGHT_RANGE.message,
                code=TournamentError.INVALID_WEIGHT_RANGE.code,
            )
        if self._has_height_limits and (
            self.initial_height < 0 or self.final_height < 0
        ):
            raise DomainException(
                TournamentError.INVALID_HEIGHT_LIMITS.message,
                code=TournamentError.INVALID_HEIGHT_LIMITS.code,
            )
        if self._has_height_limits and self.initial_height > self.final_height:
            raise DomainException(
                TournamentError.INVALID_HEIGHT_RANGE.message,
                code=TournamentError.INVALID_HEIGHT_RANGE.code,
            )

    @property
    def _has_weight_limits(self) -> bool:
        return self.initial_weight is not None and self.final_weight is not None

    @property
    def _has_height_limits(self) -> bool:
        return self.initial_height is not None and self.final_height is not None


@dataclass
class CategoryRegistration:
    """Entity representing the registration of a competitor in a category."""

    id: UUID
    competitor: Competitor
    category: Category
    tournament: Tournament
