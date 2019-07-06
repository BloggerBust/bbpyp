from enum import auto
from bbp.state_machine.model.abstract_state import AbstractState


class InterpreterState(AbstractState):
    ERROR_STATE = auto()
    START = auto()
    PARSE_TOKENS = auto()
    DISPATCH_PARSER = auto()
    EVALUATE = auto()
    REPORT_RESULT = auto()
