import heapq
from bbpyp.common.model.queue import Queue
from bbpyp.common.model.sequential_transfer_object import SequentialTransferObject
from bbpyp.common.exception.bbpyp_value_error import BbpypValueError


class SequenceQueue(Queue):

    def __init__(self, sequence_service):
        super().__init__()
        self._sequence_service = sequence_service
        self._queue = []

    def push(self, sequential_transfer_object):
        if not isinstance(sequential_transfer_object, SequentialTransferObject):
            raise BbpypValueError("sequential_transfer_object", sequential_transfer_object,
                                  f"Expected an instance of SequentialTransferObject, but received an instance of {type(sequential_transfer_object)}")
        heapq.heappush(self._queue, sequential_transfer_object)

    def pop(self):
        return self._pop() if self.is_peek_in_sequence_order() else None

    def peek(self, only_if_sequenced=True):
        peek_transfer_object = None
        if only_if_sequenced:
            if self.is_peek_in_sequence_order():
                peek_transfer_object = self._queue[0]
        else:
            peek_transfer_object = self._queue[0]
        return peek_transfer_object

    def remove(self, item):
        self._queue.remove(item)
        del item
        heapq.heapify(self._queue)

    def index_of(self, item):
        return self._queue.index(item)

    def is_peek_in_sequence_order(self):
        peek_sequential_transfer_object = self.peek(only_if_sequenced=False)
        ordered_peek_sequence_identifier = self._sequence_service.peek_sequenced_identifier(
            peek_sequential_transfer_object.sequence_name)
        return peek_sequential_transfer_object.sequence_number == ordered_peek_sequence_identifier

    @property
    def length(self):
        return len(self._queue)

    def _pop(self):
        sequential_transfer_object = heapq.heappop(self._queue)
        self._sequence_service.pop_sequenced_identifier(sequential_transfer_object.sequence_name)
        return sequential_transfer_object
