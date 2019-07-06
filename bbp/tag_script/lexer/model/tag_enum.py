from enum import auto
from bbp.state_machine.model.abstract_state import AbstractState


class TagEnum(AbstractState):
    NONE = None
    RESERVED = auto()
    NUMBER = auto()
    TAG = auto()
