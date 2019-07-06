from bbp.common.exception.bbp_exception import BbpException


class BbpKeyError(BbpException):
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
