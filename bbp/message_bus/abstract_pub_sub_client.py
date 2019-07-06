from bbp.message_bus.abstract_publisher import AbstractPublisher
from bbp.message_bus.abstract_subscriber import AbstractSubscriber


class AbstractPubSubClient(AbstractPublisher, AbstractSubscriber):
    __EVENT_QUEUE_TOPIC_POSTFIX = "__EVENT_QUEUE"

    def __init__(self, queue_service, notification_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__queue_service = queue_service
        self.__notification_service = notification_service
        self.__topic_disconnect_events = {}

        self._logger.debug("{} is composed with queue_service = {}", self, queue_service)

    def __get_event_queue_key(self, topic):
        return f"{topic}_{type(self).__EVENT_QUEUE_TOPIC_POSTFIX}"

    def open_message_queue(self, topic, disconnect_event, queue_type):
        event_queue_key = self.__get_event_queue_key(topic)
        if not self._is_message_queue_open(topic):
            self._logger.debug("opening message {} queue on topic {}, by topic {} with disconnect_event: {}",
                               queue_type, topic, self.topic, disconnect_event)
            self.__queue_service.create_queue(topic, queue_type)
            disconnect_events = {disconnect_event}
            self.__topic_disconnect_events[event_queue_key] = disconnect_events
        else:
            disconnect_events = self._get_topic_disconnect_events(topic)
            disconnect_events_length_before = len(disconnect_events)
            disconnect_events.add(disconnect_event)
            disconnect_events_length_after = len(disconnect_events)
            if disconnect_events_length_after > disconnect_events_length_before:
                self._logger.debug("For {} queue on topic {} appended disconnect event {} to event_queue_key = {}, length = {}",
                                   queue_type, topic, disconnect_event, event_queue_key, disconnect_events_length_after)

    def _get_on_queue_condition(self, topic):
        return self.__notification_service.get_notification_condition(topic)

    def _cancel_on_queue_condition(self, topic):
        self.__notification_service.cancel_notification_condition(topic)

    def _is_message_queue_open(self, topic):
        return self.__queue_service.has_queue(topic)

    def _get_next_queued_message(self, topic):
        self._logger.debug("going to get the next queued message for topic {}. length = {}",
                           topic, self.__queue_service.length(self.topic))
        return self.__queue_service.pop(topic)

    def _get_topic_disconnect_events(self, topic):
        event_queue_key = self.__get_event_queue_key(topic)
        if event_queue_key not in self.__topic_disconnect_events:
            return None
        return self.__topic_disconnect_events[event_queue_key]

    def _is_queue_empty(self, topic):
        return not self._is_message_queue_open(topic) or self.__queue_service.is_empty(topic)

    def _is_queue_poppable(self, topic):
        return not self._is_queue_empty(topic) and self.__queue_service.peek(topic) is not None

    def _are_all_queued_topic_events_set(self, topic):
        disconnect_events = self._get_topic_disconnect_events(topic)
        if disconnect_events is None:
            return False

        for disconnect_event in disconnect_events:
            if not disconnect_event.is_set():
                return False

        return True
