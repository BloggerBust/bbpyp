from enum import Flag, unique, auto


@unique
class IndentDelta(Flag):
    NONE = 0
    SAME = auto()
    INCREASE = auto()
    DECREASE = auto()
    ANY = SAME | INCREASE | DECREASE
