from uuid import uuid4


class SequenceService:

    def __init__(self, fifo_queue_factory, named_item_service):
        self._fifo_queue_factory = fifo_queue_factory
        self._named_queue = named_item_service

    def get_next_sequenced_identifier(self, sequence_name):
        if not self.has_sequence(sequence_name):
            self._new_sequence(sequence_name)
        sequence_id = uuid4().hex
        self._named_queue.get(sequence_name).push(sequence_id)
        return sequence_id

    def remove_sequenced_identifier(self, sequence_name, sequence_id):
        self._validate_sequence_does_exists(sequence_name)
        self._named_queue.get(sequence_name).remove(sequence_id)

    def peek_sequenced_identifier(self, sequence_name):
        self._validate_sequence_does_exists(sequence_name)
        return self._named_queue.get(sequence_name).peek()

    def pop_sequenced_identifier(self, sequence_name):
        self._validate_sequence_does_exists(sequence_name)
        return self._named_queue.get(sequence_name).pop()

    def compare_relative_sequence(self, sequence_name, lhs_sequence_id, rhs_sequence_id):
        self._validate_sequence_does_exists(sequence_name)

        lhs_index = self._named_queue.get(sequence_name).index_of(lhs_sequence_id)
        if lhs_sequence_id == rhs_sequence_id:
            return 0

        rhs_index = self._named_queue.get(sequence_name).index_of(rhs_sequence_id)
        return 1 if lhs_index > rhs_index else -1

    def has_sequence(self, sequence_name):
        return self._named_queue.has(sequence_name)

    def _new_sequence(self, sequence_name):
        self._validate_sequence_does_not_exists(sequence_name)
        self._named_queue.set(sequence_name, self._fifo_queue_factory())

    def _validate_sequence_does_exists(self, sequence_name):
        self._named_queue.validate_has_name(sequence_name, "sequence does not exist")

    def _validate_sequence_does_not_exists(self, sequence_name):
        self._named_queue.validate_does_not_have_name(sequence_name, "sequence already exists")
