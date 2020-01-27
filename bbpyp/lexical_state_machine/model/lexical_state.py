from enum import auto
from bbpyp.state_machine.model.abstract_state import AbstractState


class LexicalState(AbstractState):
    ERROR_STATE = auto()
    START = auto()
    PARSE_TAGS = auto()
    DISPATCH_TOKENS = auto()
