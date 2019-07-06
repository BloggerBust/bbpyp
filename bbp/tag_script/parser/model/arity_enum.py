from enum import Flag, unique, auto


@unique
class ArityEnum(Flag):
    ONE = auto()
    TWO = auto()
    ANY = ONE | TWO

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
