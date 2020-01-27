from logging import LoggerAdapter


class BasicLogAdapter(LoggerAdapter):
    def __init__(self, logger, log_message_factory, extra=None):
        super().__init__(logger, extra or {})
        self._log_message_factory = log_message_factory

    def log(self, level, log_message, *args, **kwargs):
        if self.isEnabledFor(level):
            log_message, kwargs = self.process(log_message, kwargs)

            if isinstance(log_message, str):
                log_message = self._log_message_factory(log_message, args)

            self.logger._log(level, log_message, (), **kwargs)
