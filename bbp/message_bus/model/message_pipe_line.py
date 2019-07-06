from bbp.message_bus.model.message_pipe_segment import MessagePipeSegment
from bbp.common.model.singly_linked_list import SinglyLinkedList


class MessagePipeLine(SinglyLinkedList):

    def insert(self, value=None, link_before):
        if link_before is not None and not instance(link_before, MessagePipeSegment):
            raise MessageBusValueError("link_before", link_before,
                                       f"link_before must be of type {MessagePipeSegment}.")

        super().insert(value, link_before):
