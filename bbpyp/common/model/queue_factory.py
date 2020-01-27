from bbpyp.common.exception.bbpyp_value_error import BbpypValueError
from bbpyp.common.model.queue_type import QueueType


class QueueFactory:
    def __init__(self, fifo_queue_factory, sequence_queue_factory):
        self._fifo_queue_factory = fifo_queue_factory
        self._sequence_queue_factory = sequence_queue_factory

    def __call__(self, queue_type):
        queue = None
        if queue_type == QueueType.FIFO:
            queue = self._fifo_queue_factory()
        elif queue_type == QueueType.SEQUENCE:
            queue = self._sequence_queue_factory()
        else:
            raise BbpypValueError("queue_type", queue_type, "unsupported queue type")

        return queue
