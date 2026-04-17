from dataclasses import dataclass, field
from uuid import UUID
from typing import List, Optional
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
class PhysicalRequirement:
    """Value Object representing physical requirements for a category-modality."""
    id: UUID
    initial_weight: Optional[float] = None
    final_weight: Optional[float] = None
    initial_height: Optional[float] = None
    final_height: Optional[float] = None

    def __post_init__(self):
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
class Category:
    """Entity defining a competition category (Age, Sex, Rank)."""

    id: UUID
    ages: List[int]
    special_condition: bool
    sexes: List[Sex]
    ranks: List[Rank]
    modalities: List["CategoryModality"] = field(default_factory=list)

    def __post_init__(self):
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

    def is_eligible_base(self, competitor: Competitor) -> dict:
        """Checks only the base requirements of the category (Age, Sex, Rank)."""
        return {
            "age_mismatch": competitor.age not in self.ages,
            "special_condition_mismatch": competitor.special_condition != self.special_condition,
            "sex_mismatch": competitor.sex not in self.sexes,
            "rank_mismatch": self.ranks and competitor.rank not in self.ranks,
        }


@dataclass
class CategoryModality:
    """Linking entity between Category and Modality with specific physical requirements."""
    id: UUID
    category: Category
    modality: Modality
    physical_requirement: Optional[PhysicalRequirement] = None

    @property
    def ages(self) -> List[int]:
        return self.category.ages

    @property
    def sexes(self) -> List[Sex]:
        return self.category.sexes

    @property
    def ranks(self) -> List[Rank]:
        return self.category.ranks

    def get_eligibility_failures(self, competitor: Competitor) -> dict:
        """Determines why a competitor is not eligible for this category-modality."""
        failures = self.category.is_eligible_base(competitor)
        failures.update({
            "weight_mismatch": False,
            "height_mismatch": False,
        })

        if self.physical_requirement:
            req = self.physical_requirement
            if req._has_weight_limits:
                if competitor.weight is None or not (
                    req.initial_weight <= competitor.weight <= req.final_weight
                ):
                    failures["weight_mismatch"] = True

            if req._has_height_limits:
                if competitor.height is None or not (
                    req.initial_height <= competitor.height <= req.final_height
                ):
                    failures["height_mismatch"] = True

        return failures

    def is_eligible(self, competitor: Competitor) -> bool:
        """Verifies if a competitor meets all the conditions to enter this category-modality."""
        failures = self.get_eligibility_failures(competitor)
        return not any(failures.values())


@dataclass
class CategoryRegistration:
    """Entity representing the registration of a competitor in a category-modality."""

    id: UUID
    competitor: Competitor
    category_modality: CategoryModality
    tournament: Tournament
