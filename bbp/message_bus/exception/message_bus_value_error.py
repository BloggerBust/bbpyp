from bbp.common.exception.bbp_value_error import BbpValueError
from bbp.message_bus.exception.message_bus_error import MessageBusError


class MessageBusValueError(MessageBusError, BbpValueError):
    pass
