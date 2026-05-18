from enum import Enum

class CreateVariablesSetRequestMode(str, Enum):
    COLUMN = "COLUMN"
    ROW = "ROW"
    SEQUENTIAL = "SEQUENTIAL"

    def __str__(self) -> str:
        return str(self.value)
