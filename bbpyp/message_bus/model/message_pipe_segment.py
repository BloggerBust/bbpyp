from bbpyp.message_bus.model.message_pipe import MessagePipe
from bbpyp.common.model.single_link_node import SingleLinkNode


class MessagePipeSegment(SingleLinkNode):
    def __init__(self, message_pipe, *args, **kwargs):
        super().__init__(value=message_pipe, *args, **kwargs)

        if not isinstance(message_pipe, MessagePipe):
            raise MessageBusValueError("message_pipe", message_pipe,
                                       f"message_pipe must be of type {type(MessagePipe)}.")
