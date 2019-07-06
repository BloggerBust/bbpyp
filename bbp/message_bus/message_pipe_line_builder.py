from bbp.message_bus.exception.message_bus_value_error import MessageBusValueError
from bbp.message_bus.abstract_publisher import AbstractPublisher
from bbp.message_bus.abstract_subscriber import AbstractSubscriber


class MessagePipeLineBuilder:
    def __init__(self, linked_list, message_pipe_factory):
        self._message_pipe_factory = message_pipe_factory
        self._pipe_line = linked_list

        self._topic = None
        self._publishers = []
        self._subscribers = []

    def for_topic(self, topic):
        self._validate_topic(topic)
        self._topic = topic
        return self

    def with_publisher(self, publisher):
        self._validate_publisher(publisher)
        self._publishers.append(publisher)
        return self

    def with_subscriber(self, subscriber, **kwargs):
        self._validate_subscriber(subscriber)
        self._subscribers.append((subscriber, kwargs))
        return self

    def append_pipe(self):
        if self._topic is None and len(self._publishers) == 0 and len(self._subscribers) == 0:
            return self

        self._validate_pending_components()

        message_pipe = self._message_pipe_factory(
            self._topic, self._publishers.copy(), self._subscribers.copy())

        self._pipe_line.append(message_pipe)

        self._topic = None
        self._publishers.clear()
        self._subscribers.clear()

        return self

    def build(self):
        return self.append_pipe()._pipe_line

    def _validate_topic(self, topic):
        if not isinstance(topic, str):
            raise MessageBusValueError(
                "topic", topic, f"The topic provided for the pipeline must be of type [{str}], but was of type [{type(topic)}]")

    def _validate_publisher(self, publisher):
        if not isinstance(publisher, AbstractPublisher):
            raise MessageBusValueError("publisher", publisher,
                                       f"The publisher being added to the pipeline for topic [{self._topic}] must be of type [{AbstractPublisher}], but was of type [{type(publisher)}]")

    def _validate_publishers(self, publishers):
        if not len(publishers):
            raise MessageBusValueError("publishers", publishers,
                                       f"The publisher collection being added to the pipeline for topic [{self._topic}] must be none empty")
        for publisher in publishers:
            self._validate_publisher(publisher)

    def _validate_subscriber(self, subscriber):
        if not isinstance(subscriber, AbstractSubscriber):
            raise MessageBusValueError("subscriber", subscriber,
                                       f"The subscriber being added to the pipeline for topic [{self._topic}] must be of type [{AbstractSubscriber}], but was of type [{type(subscriber)}]")

    def _validate_subscribers(self, subscribers):
        if not len(subscribers):
            raise MessageBusValueError("subscribers", subscribers,
                                       f"The subscriber collection being added to the pipeline for topic [{self._topic}] must be none empty")
        for subscriber, _ in subscribers:
            self._validate_subscriber(subscriber)

    def _validate_pending_components(self):
        self._validate_topic(self._topic)
        self._validate_publishers(self._publishers)
        self._validate_subscribers(self._subscribers)
