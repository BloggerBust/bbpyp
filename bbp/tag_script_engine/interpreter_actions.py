from bbp.interpreter_state_machine.abstract_interpreter_actions import AbstractInterpreterActions
from bbp.tag_script_engine.model.topic import Topic


class InterpreterActions (AbstractInterpreterActions):
    def __init__(self, logger, parser_combinator, queue_service, notification_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__logger = logger
        self.__parser_combinator = parser_combinator
        self.__queue_service = queue_service
        self.__notification_service = notification_service

    def parse(self, tokens):
        return self.__parser_combinator(tokens, 0)

    def dispatch(self, message):
        self.__logger.debug("dispatching from interpreter actions on topic {} for message id {}",
                            Topic.EVALUATE.value, message.sequence_number)
        self.__publish(Topic.EVALUATE.value, message)

    def evaluate(self, parser, frame):
        return parser.eval_and_return_result(frame)

    def report(self, parser, frame):
        result = parser.get_result_aggregate(frame)
        self.__publish(Topic.REPORT.value, result)

    def __publish(self, topic, message):
        self.__queue_service.push(topic, message)
        if self.__queue_service.peek(topic) is not None:
            self.__notification_service.notify(topic, self.__queue_service.length(topic))
