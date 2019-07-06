from abc import ABC, abstractmethod


class Queue(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def push(self, item):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def peek(self):
        pass

    @abstractmethod
    def remove(self, item):
        pass

    @abstractmethod
    def index_of(self, item):
        pass

    @property
    @abstractmethod
    def length(self):
        pass

    @property
    def is_empty(self):
        return self.length == 0
