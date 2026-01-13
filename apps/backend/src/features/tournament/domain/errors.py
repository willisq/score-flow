from enum import Enum


class TournamentError(Enum):
    INVALID_MODALITY_NAME = ("INVALID_MODALITY_NAME", "Modality name cannot be empty")
    INVALID_TOURNAMENT_DESCRIPTION = (
        "INVALID_TOURNAMENT_DESCRIPTION",
        "Tournament description cannot be empty",
    )
    INVALID_CATEGORY_NAME = ("INVALID_CATEGORY_NAME", "Category name cannot be empty")
    INVALID_CATEGORY_MODALITY = (
        "INVALID_CATEGORY_MODALITY",
        "Category must have a modality",
    )
    INVALID_AGE_LIMITS = ("INVALID_AGE_LIMITS", "Age limits cannot be negative")
    INVALID_AGE_RANGE = (
        "INVALID_AGE_RANGE",
        "Initial age cannot be greater than final age",
    )

    @property
    def code(self) -> str:
        return self.value[0]

    @property
    def message(self) -> str:
        return self.value[1]
