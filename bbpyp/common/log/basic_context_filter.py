import logging
from random import choice


class BasicContextFilter(logging.Filter):

    def __init__(self, context_service):
        self._context_service = context_service

    def filter(self, record):
        if hasattr(record, "CONTEXT_ID"):
            record.CONTEXT_ID = self._context_service.get_context_variable("CONTEXT_ID")
        return True
