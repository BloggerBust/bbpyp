from abc import ABC, abstractmethod


class AbstractInterpreterActions(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        self_type = type(self)
        return f"{self_type.__module__}.{self_type.__name__}"

    @abstractmethod
    def parse(self, tokens):
        raise NotImplementedError(
            f"Abstract method {self}.parser must be implemented by a subclass")

    @abstractmethod
    def dispatch(self, message):
        raise NotImplementedError(
            f"Abstract method {self}.dispatch must be implemented by a subclass")

    @abstractmethod
    def evaluate(self, parser, frame):
        raise NotImplementedError(
            f"Abstract method {self}.evaluate must be implemented by a subclass")
