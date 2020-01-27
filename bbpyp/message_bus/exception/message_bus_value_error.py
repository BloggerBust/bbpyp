from bbpyp.common.exception.bbpyp_value_error import BbpypValueError
from bbpyp.message_bus.exception.message_bus_error import MessageBusError


class MessageBusValueError(MessageBusError, BbpypValueError):
    pass
