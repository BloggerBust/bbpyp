from enum import Flag, unique, auto

@unique
class PrecedenceLevelEnum(Flag):
    ZERO = auto()
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    ALL = ZERO|ONE|TWO|THREE|FOUR|FIVE|SIX
    
    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.value == other.value
            
    def __ge__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.value >= other.value

    def __gt__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.value > other.value

    def __le__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.value <= other.value

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.value < other.value
