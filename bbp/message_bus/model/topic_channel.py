from bbp.message_bus.abstract_publisher import AbstractPublisher
from bbp.message_bus.abstract_subscriber import AbstractSubscriber

from copy import deepcopy


class TopicChannel:
    __CONTEXT_ID_KEY = "CONTEXT_ID"
    __LINKED_DISCONNECT_EVENT_KEY = "__LINKED_DISCONNECT_EVENT_KEY"
    __LINKED_TOPIC_KEY = "__LINKED_TOPIC_KEY"

    def __init__(self, topic, logger, channel_topic_config, channel_topic_config_default, async_service, context_service):
        self._started = False
        self._topic = topic
        self._logger = logger
        self._async_service = async_service
        self._context_service = context_service
        self._publisher_connection_source = None
        self._subscriber_connection_source = None
        self._publisher_connection_clones = []
        self._subscriber_connection_clones = []
        self._publishers = []
        self._subscribers = []

        _channel_topic_config = deepcopy(
            channel_topic_config[topic]) if topic in channel_topic_config else {}

        for key, val in channel_topic_config_default.items():
            if key not in _channel_topic_config:
                _channel_topic_config[key] = deepcopy(val)

        self._number_of_publisher_clones = _channel_topic_config["publish_concurrency"] + 1
        self._number_of_subscriber_clones = _channel_topic_config["subscribe_concurrency"] + 1
        self._subscribe_queue_type = _channel_topic_config["subscribe_queue_type"]

        self._publisher_connect_event = self._async_service.create_event()
        self._subscriber_connect_event = self._async_service.create_event()
        self._publisher_disconnect_event = self._async_service.create_event()
        self._subscriber_disconnect_event = self._async_service.create_event()

    def _create_connections(self):
        publisher_connection, subscriber_connection = self._async_service.create_channel()
        self._publisher_connection_source = publisher_connection
        self._subscriber_connection_source = subscriber_connection
        self._publisher_connection_clones = [self._publisher_connection_source.clone(
        ) for i in range(0, self._number_of_publisher_clones)]
        self._subscriber_connection_clones = [self._subscriber_connection_source.clone(
        ) for i in range(0, self._number_of_subscriber_clones)]

    def register_publisher(self, publisher, **kwargs):
        if not isinstance(publisher, AbstractPublisher):
            raise MessageBusValueError("publisher", publisher,
                                       f"The publisher being registered for topic [{self.topic}] must be of type [{type(AbstractPublisher)}], but was of type [{type(publisher)}]")

        self._publishers.append((publisher, kwargs))

    def register_subscriber(self, subscriber, **kwargs):
        if not isinstance(subscriber, AbstractSubscriber):
            raise MessageBusValueError("subscriber", subscriber,
                                       f"The subscriber being registered for topic [{self.topic}] must be of type [{type(AbstractSubscriber)}], but was of type [{type(subscriber)}]")

        self._subscribers.append((subscriber, kwargs))

    async def start(self, channel_context):
        if self._started:
            await self._async_service.sleep()
            return

        self._create_connections()

        context_id = self._context_service.get_context_variable(type(self).__CONTEXT_ID_KEY)
        self._logger.info("[{}] starting connections", context_id)

        for publisher, kwargs in self._publishers:
            publisher.connect_event = self._publisher_connect_event
            publisher.disconnect_event = self._publisher_disconnect_event
            for cloned_connection in self._publisher_connection_clones:
                self._context_service.set_context_variable(
                    type(self).__CONTEXT_ID_KEY, f"{context_id}P")
                self._start_publisher(channel_context, publisher, cloned_connection, **kwargs)

        for subscriber, kwargs in self._subscribers:
            subscriber.connect_event = self._subscriber_connect_event
            subscriber.disconnect_event = self._subscriber_disconnect_event
            if self.__linked_from_channel_disconnect_event is not None:
                self._logger.debug(
                    "opening subscriber message queue link: {} --> {}", subscriber.topic, self.__linked_to_channel_topic)
                subscriber.open_message_queue(
                    self.__linked_to_channel_topic, self.__linked_from_channel_disconnect_event, self._subscribe_queue_type)

            for cloned_connection in self._subscriber_connection_clones:
                self._context_service.set_context_variable(
                    type(self).__CONTEXT_ID_KEY, f"{context_id}S")
                self._start_subscriber(channel_context, subscriber, cloned_connection,
                                       message_queue_topic=self.__linked_to_channel_topic, **kwargs)

        self.__linked_from_channel_disconnect_event = None
        self.__linked_to_channel_topic = None
        self._started = True

    async def stop(self):
        context_id = self._context_service.get_context_variable(
            type(self).__LINKED_DISCONNECT_EVENT_KEY)
        self._logger.info(
            "[{}] waiting for topic {} publisher connections to close...", context_id, self.topic)
        await self._publisher_disconnect_event.wait()
        await self._publisher_connection_source.aclose()

        self._logger.info(
            "[{}] waiting for topic {} subscriber connections to close...", context_id, self.topic)
        await self._subscriber_disconnect_event.wait()
        await self._subscriber_connection_source.aclose()

        self._logger.info("all connections for topic {} have been closed.", self.topic)

    def open_linked_topics(self, linked_to_topic):
        self._logger.debug("opening linked topic: {} --> {}", self.topic, linked_to_topic)
        self.__linked_from_channel_disconnect_event = self._subscriber_disconnect_event
        self.__linked_to_channel_topic = linked_to_topic

    def _start_publisher(self, channel_context, publisher, connection, **kwargs):
        publisher.topic = self.topic
        self._logger.debug(
            "{} connecting publisher {} with kwargs: {}", self._context_service.get_context_variable(type(self).__CONTEXT_ID_KEY), publisher, kwargs)

        channel_context.start_soon(publisher.connect_publisher, connection, kwargs)

    def _start_subscriber(self, channel_context, subscriber, connection, **kwargs):
        subscriber.topic = self.topic
        self._logger.debug(
            "{}: connecting subscriber {} with kwargs: {}", self._context_service.get_context_variable(type(self).__CONTEXT_ID_KEY), subscriber, kwargs)

        channel_context.start_soon(subscriber.connect_subscriber,
                                   connection, self._publisher_connect_event, self._publisher_disconnect_event, kwargs)

    @property
    def topic(self):
        return self._topic

    @property
    def __linked_from_channel_disconnect_event(self):
        return self._context_service.get_context_variable(type(self).__LINKED_DISCONNECT_EVENT_KEY)

    @__linked_from_channel_disconnect_event.setter
    def __linked_from_channel_disconnect_event(self, disconnect_event):
        self._context_service.set_context_variable(
            type(self).__LINKED_DISCONNECT_EVENT_KEY, disconnect_event)

    @property
    def __linked_to_channel_topic(self):
        return self._context_service.get_context_variable(type(self).__LINKED_TOPIC_KEY)

    @__linked_to_channel_topic.setter
    def __linked_to_channel_topic(self, topic):
        self._context_service.set_context_variable(
            type(self).__LINKED_TOPIC_KEY, topic)
