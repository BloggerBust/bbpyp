from collections import deque
from bbpyp.common.model.queue import Queue


class FifoQueue(Queue):
    def __init__(self):
        super().__init__()
        self._queue = deque()

    def push(self, item):
        self._queue.append(item)

    def pop(self):
        return self._queue.popleft()

    def peek(self):
        return self._queue[0]

    def remove(self, item):
        self._queue.remove(item)

    def index_of(self, item):
        return self._queue.index(item)

    @property
    def length(self):
        return len(self._queue)
