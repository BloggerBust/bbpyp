from abc import abstractmethod


class AbstractLexicalActions():

    def __repr__(self):
        self_type = type(self)
        return f"{self_type.__module__}.{self_type.__name__}"

    def __str__(self):
        return self.__repr__()

    @abstractmethod
    def tokenize(self, expression):
        raise NotImplementedError(
            f"Abstract method {self}.tokenize must be implemented by a subclass")

    @abstractmethod
    def dispatch(self, message):
        raise NotImplementedError(
            f"Abstract method {self}.tokenize must be implemented by a subclass")
