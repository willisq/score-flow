from enum import Enum


class BracketError(Enum):
    INVALID_ROUND_DESCRIPTION = (
        "INVALID_ROUND_DESCRIPTION",
        "Round description cannot be empty",
    )
    INVALID_MATCH_WINNER = (
        "INVALID_MATCH_WINNER",
        "Competitor is not part of this match",
    )
    ROUND_NOT_COMPLETE = ("ROUND_NOT_COMPLETE", "Round is not complete")

    @property
    def code(self) -> str:
        return self.value[0]

    @property
    def message(self) -> str:
        return self.value[1]
