import uuid
from abc import abstractmethod


class BusParticipant:
    __ID_KEY = "PARTICIPANT_ID_KEY"
    __DISCONNECT_KEY = "DISCONNECT_KEY"
    __CONNECT_KEY = "CONNECT_KEY"
    __TOPIC_KEY = "TOPIC_KEY"

    def __init__(self, logger, context_service, async_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logger
        self._context_service = context_service
        self._logger.debug("{} is composed with context_service = {}", self, context_service)
        self._async_service = async_service

    def __repr__(self):
        return f"{self.__class__.__name__}[{self.participant_id}]()"

    def __str__(self):
        return self.__repr__()

    @abstractmethod
    def _receive_context_parameters(*args, **kwargs):
        pass

    @property
    def participant_id(self):
        current_id = self._context_service.get_context_variable(type(self).__ID_KEY)
        if current_id is None:
            self._create_new_participant_id()
        return self._context_service.get_context_variable(type(self).__ID_KEY)

    def _create_new_participant_id(self):
        self._context_service.set_context_variable(type(self).__ID_KEY, uuid.uuid4().hex)

    @property
    def disconnect_event(self):
        return self._context_service.get_context_variable(type(self).__DISCONNECT_KEY)

    @disconnect_event.setter
    def disconnect_event(self, event):
        self._context_service.set_context_variable(type(self).__DISCONNECT_KEY, event)

    @property
    def connect_event(self):
        return self._context_service.get_context_variable(type(self).__CONNECT_KEY)

    @connect_event.setter
    def connect_event(self, event):
        self._context_service.set_context_variable(type(self).__CONNECT_KEY, event)

    @property
    def topic(self):
        return self._context_service.get_context_variable(type(self).__TOPIC_KEY)

    @topic.setter
    def topic(self, topic):
        self._create_new_participant_id()
        return self._context_service.set_context_variable(type(self).__TOPIC_KEY, topic)
