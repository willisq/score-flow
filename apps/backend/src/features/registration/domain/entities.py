from dataclasses import dataclass
from uuid import UUID
from src.core.common.exceptions import DomainException
from .errors import RegistrationError


@dataclass
class Sex:
    """Value Object representing biological sex."""

    id: UUID
    name: str

    def __post_init__(self):
        if not self.name:
            raise DomainException(
                RegistrationError.INVALID_SEX_NAME.message,
                code=RegistrationError.INVALID_SEX_NAME.code,
            )


@dataclass
class Person:
    """Base Entity for any person in the system."""

    id: UUID
    first_name: str
    last_name: str

    def __post_init__(self):
        if not self.first_name:
            raise DomainException(
                RegistrationError.INVALID_FIRST_NAME.message,
                code=RegistrationError.INVALID_FIRST_NAME.code,
            )
        if not self.last_name:
            raise DomainException(
                RegistrationError.INVALID_LAST_NAME.message,
                code=RegistrationError.INVALID_LAST_NAME.code,
            )

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass
class Academy:
    """Entity representing a training academy."""

    id: UUID
    name: str
    instructor: Person

    def __post_init__(self):
        if not self.name:
            raise DomainException(
                RegistrationError.INVALID_ACADEMY_NAME.message,
                code=RegistrationError.INVALID_ACADEMY_NAME.code,
            )

        if not self.instructor:
            raise DomainException(
                RegistrationError.INVALID_ACADEMY_INSTRUCTOR.message,
                code=RegistrationError.INVALID_ACADEMY_INSTRUCTOR.code,
            )


@dataclass
class Rank:
    """Entity representing a competitor's rank."""

    id: UUID
    name: str
    classification: int
    is_black_belt: bool

    def __post_init__(self):
        if not self.name:
            raise DomainException(
                RegistrationError.INVALID_RANK_NAME.message,
                code=RegistrationError.INVALID_RANK_NAME.code,
            )

        if self.classification <= 0:
            raise DomainException(
                RegistrationError.INVALID_RANK_CLASSIFICATION.message,
                code=RegistrationError.INVALID_RANK_CLASSIFICATION.code,
            )


@dataclass
class Competitor(Person):
    """Entity representing a competitor, extending Person."""

    id: UUID
    academy: Academy
    rank: Rank
    sex: Sex
    weight: float | None = None
    height: float | None = None
    age: int | None = None
    special_condition: bool = False

    def __post_init__(self):
        super().__post_init__()

        if self.weight is not None and self.weight <= 0:
            raise DomainException(
                RegistrationError.INVALID_WEIGHT.message,
                code=RegistrationError.INVALID_WEIGHT.code,
            )

        if self.height is not None and self.height <= 0:
            raise DomainException(
                RegistrationError.INVALID_HEIGHT.message,
                code=RegistrationError.INVALID_HEIGHT.code,
            )
