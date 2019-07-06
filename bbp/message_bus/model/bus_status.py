from enum import Enum, auto


class BusStatus(Enum):
    STOPPED = auto()
    STARTED = auto()
    SHUTTING_DOWN = auto()
