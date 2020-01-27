from enum import Enum, auto


class QueueType(Enum):
    FIFO = auto()
    SEQUENCE = auto()
