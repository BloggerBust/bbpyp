from bbp.common.model.equatable_state import EquatableState


class Result(EquatableState):
    def __init__(self, value, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = value
        self._position = position

    def __repr__(self):
        return f"{type(self).__name__}({self.value}, {self.position})"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
