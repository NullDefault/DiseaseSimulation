from enum import Enum, auto


class States(Enum):
    AWAIT_INPUT = auto()
    CONTINUE_TO_NEXT_STATE = auto()
