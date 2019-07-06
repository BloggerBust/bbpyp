from bbp.common.model.sequential_transfer_object import SequentialTransferObject


class Message(SequentialTransferObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"Message #: {self.sequence_number}, payload: {self.payload}, meta: {self.meta}"
