

class BbpypException(Exception):
    def __init__(self, what, reason, *args, inner_exception=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._what = what
        self._reason = reason
        self._inner_exception = inner_exception

    def __repr__(self):
        representation = f"{self.who}: {self.what}: {self.why}"
        if self._inner_exception:
            representation += f"\nCaused By:{self._inner_exception}"
        return representation

    def __str__(self):
        return self.__repr__()

    @property
    def who(self):
        return f"{type(self).__name__}"

    @property
    def what(self):
        return self._what

    @property
    def why(self):
        return self._reason

    @property
    def inner_exception(self):
        return self._inner_exception
