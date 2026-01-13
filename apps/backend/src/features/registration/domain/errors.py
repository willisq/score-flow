from enum import Enum


class RegistrationError(Enum):
    INVALID_SEX_NAME = ("INVALID_SEX_NAME", "Sex name cannot be empty")
    INVALID_FIRST_NAME = ("INVALID_FIRST_NAME", "First name cannot be empty")
    INVALID_LAST_NAME = ("INVALID_LAST_NAME", "Last name cannot be empty")
    INVALID_ACADEMY_NAME = ("INVALID_ACADEMY_NAME", "Academy name cannot be empty")
    INVALID_ACADEMY_INSTRUCTOR = (
        "INVALID_ACADEMY_INSTRUCTOR",
        "Academy must have an instructor",
    )
    INVALID_RANK_NAME = ("INVALID_RANK_NAME", "Rank name cannot be empty")
    INVALID_WEIGHT = ("INVALID_WEIGHT", "Weight must be positive")
    INVALID_HEIGHT = ("INVALID_HEIGHT", "Height must be positive")

    @property
    def code(self) -> str:
        return self.value[0]

    @property
    def message(self) -> str:
        return self.value[1]