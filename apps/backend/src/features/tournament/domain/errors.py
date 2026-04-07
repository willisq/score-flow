from enum import Enum


class TournamentError(Enum):
    INVALID_MODALITY_NAME = ("INVALID_MODALITY_NAME", "Modality name cannot be empty")
    INVALID_TOURNAMENT_DESCRIPTION = (
        "INVALID_TOURNAMENT_DESCRIPTION",
        "Tournament description cannot be empty",
    )
    INVALID_CATEGORY_MODALITY = (
        "INVALID_CATEGORY_MODALITY",
        "Category must have a modality",
    )
    INVALID_AGE_LIST = ("INVALID_AGE_LIST", "Age list cannot be empty")
    INVALID_AGE_LIMITS = ("INVALID_AGE_LIMITS", "Age limits cannot be negative or zero")
    INVALID_AGE_RANGE = (
        "INVALID_AGE_RANGE",
        "Initial age cannot be greater than final age",
    )
    INVALID_WEIGHT_LIMITS = (
        "INVALID_WEIGHT_LIMITS",
        "Weight limits cannot be negative",
    )
    INVALID_WEIGHT_RANGE = (
        "INVALID_WEIGHT_RANGE",
        "Initial weight cannot be greater than final weight",
    )
    INVALID_HEIGHT_LIMITS = (
        "INVALID_HEIGHT_LIMITS",
        "Height limits cannot be negative",
    )
    INVALID_HEIGHT_RANGE = (
        "INVALID_HEIGHT_RANGE",
        "Initial height cannot be greater than final height",
    )

    @property
    def code(self) -> str:
        return self.value[0]

    @property
    def message(self) -> str:
        return self.value[1]
