from bbp.common.model.queue_type import QueueType


class QueueService:
    def __init__(self, queue_factory, named_item_service, metric_service):
        self._queue_factory = queue_factory
        self._named_queue = named_item_service
        self._metric_service = metric_service

    def create_queue(self, queue_name, queue_type=QueueType.FIFO):
        if self.has_queue(queue_name):
            return
        self._named_queue.set(queue_name, self._queue_factory(queue_type))

    def push(self, queue_name, item):
        named_queue = self._get_named_queue(queue_name, f"Unable to queue the item: {item}")
        named_queue.push(item)
        self._update_named_queue_length_metric(queue_name)

    def pop(self, queue_name):
        named_queue = self._get_named_queue(queue_name, f"Unable to pop the non existent queue.")
        item = named_queue.pop()
        self._update_named_queue_length_metric(queue_name)
        return item

    def peek(self, queue_name):
        named_queue = self._get_named_queue(queue_name, f"Unable to peek the non existent queue.")
        return named_queue.peek()

    def remove(self, queue_name, item):
        named_queue = self._get_named_queue(
            queue_name, f"Unable to remove an item from the non existent queue.")
        item = named_queue.remove(item)
        self._update_named_queue_length_metric(queue_name)
        return item

    def length(self, queue_name):
        named_queue = self._get_named_queue(
            queue_name, f"Unable to get the length of the non existent queue.")
        return named_queue.length

    @property
    def queue_names(self):
        return self._named_queue.names

    def is_empty(self, queue_name):
        named_queue = self._get_named_queue(
            queue_name, f"Unable to check if non existent queue is empty.")
        return named_queue.is_empty

    def has_queue(self, queue_name):
        return self._named_queue.has(queue_name)

    def _get_named_queue(self, queue_name, failure_message):
        return self._named_queue.get_with_validation(queue_name, f"Named queue not found. {failure_message}")

    def _update_named_queue_length_metric(self, queue_name):
        self._metric_service.record_numeric_value(
            f"{queue_name}.queue.length", self.length(queue_name))
