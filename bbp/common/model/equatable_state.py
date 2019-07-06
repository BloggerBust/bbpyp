from abc import ABC


class EquatableState(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))
