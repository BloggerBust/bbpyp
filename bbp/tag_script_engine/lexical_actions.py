from bbp.lexical_state_machine.abstract_lexical_actions import AbstractLexicalActions
from bbp.tag_script_engine.model.topic import Topic


class LexicalActions(AbstractLexicalActions):

    def __init__(self, logger, lexer, queue_service, notification_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__logger = logger
        self.__lexer = lexer
        self.__logger.debug("lexical actions is composed with queue_service = {}", queue_service)
        self.__queue_service = queue_service
        self.__notification_service = notification_service

    def tokenize(self, expression):
        return self.__lexer.tokenize(expression)

    def dispatch(self, message):
        self.__publish(Topic.PARSE.value, message)

    def __publish(self, topic, message):
        self.__queue_service.push(topic, message)
        self.__notification_service.notify(topic, self.__queue_service.length(topic))
