from bbpyp.common.exception.bbpyp_exception import BbpypException


class BbpypValueError(BbpypException):
    def __init__(self, name, value, *args, **kwargs):
        super().__init__(f"{name}={value}", *args, **kwargs)

        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value
