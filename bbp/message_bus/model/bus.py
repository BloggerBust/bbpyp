from collections import deque
from bbp.message_bus.model.bus_status import BusStatus


class Bus:
    __CONTEXT_ID_KEY = "CONTEXT_ID"

    def __init__(self, logger, topic_channel_factory, async_service, context_service, *args, **kwargs):
        self._logger = logger
        self._topic_channel_factory = topic_channel_factory
        self._async_service = async_service
        self._context_service = context_service
        self._bus_status = BusStatus.STOPPED
        self._topic_channel_lookup = {}
        self._pending_topic_channels = deque()
        self._started_topic_channels = deque()

    def _create_topic_channel(self, topic):
        topic_channel = self._topic_channel_factory(topic)
        self._topic_channel_lookup[topic] = topic_channel
        self._pending_topic_channels.append(topic_channel)

    def _has_pending_topic_channels(self):
        return len(self._pending_topic_channels)

    def _peek_pending_topic_channel(self):
        return self._pending_topic_channels[0] if self._has_pending_topic_channels() else None

    def _get_pending_topic_channel(self):
        return self._pending_topic_channels.popleft()

    def _has_started_topic_channels(self):
        return len(self._started_topic_channels)

    def _peek_started_topic_channel(self):
        return self._started_topic_channels[0] if self._has_started_topic_channels() else None

    def _get_next_started_topic_channel(self):
        return self._started_topic_channels.popleft()

    def register_topic_publisher(self, topic, publisher, **kwargs):
        if topic not in self._topic_channel_lookup:
            self._create_topic_channel(topic)

        self._topic_channel_lookup[topic].register_publisher(publisher, **kwargs)
        return self

    def register_topic_subscriber(self, topic, subscriber, **kwargs):
        if topic not in self._topic_channel_lookup:
            self._create_topic_channel(topic)

        self._topic_channel_lookup[topic].register_subscriber(subscriber, **kwargs)
        return self

    async def start_bus(self, bus_link, depth=0):
        self._bus_status = BusStatus.STARTED

        if bus_link:
            linked_bus = bus_link.value
            does_linked_bus_need_starting = not bus_link.value.is_bus_running
        else:
            linked_bus = None
            does_linked_bus_need_starting = False

        async with self._async_service.create_channel_context() as channel_context:
            while True:
                if self._has_pending_topic_channels():
                    topic_channel = self._get_pending_topic_channel()

                    topic = topic_channel.topic
                    topic_prefix = topic[:topic.rfind(".")]
                    context_id = f"[{topic_prefix}]D[{depth}]"
                    self._context_service.set_context_variable(Bus.__CONTEXT_ID_KEY, context_id)
                    self._logger.debug("starting channel_context")

                    if self._has_pending_topic_channels():
                        linked_next_topic = self._peek_pending_topic_channel().topic
                        self._logger.debug(
                            "at depth {} registering topic channel to open linked topics {} --> {}", depth, topic, linked_next_topic)
                        topic_channel.open_linked_topics(linked_next_topic)
                    elif linked_bus:
                        linked_next_topic = linked_bus._peek_pending_topic_channel().topic
                        self._logger.debug(
                            "at depth {} registering topic channel to open linked topics {} --> {} transcending linked bus", depth, topic, linked_next_topic)
                        topic_channel.open_linked_topics(linked_next_topic)

                    await topic_channel.start(channel_context)
                    self._started_topic_channels.append(topic_channel)
                    self._logger.debug("channel_context started. has_pending = {}, does_linked_bus_need_starting = {}",
                                       self._has_pending_topic_channels(), does_linked_bus_need_starting)

                elif does_linked_bus_need_starting:

                    self._logger.debug(
                        "starting linked bus for context {}, topic: {}", context_id, topic)

                    next_bus_link = bus_link.next_link
                    channel_context.start_soon(linked_bus.start_bus, next_bus_link, depth + 1)
                    does_linked_bus_need_starting = False
                else:
                    break

            self._logger.debug("bus is stopped. closing channels")
            await self._close_channels(bus_link, depth)

    async def _close_channels(self, bus_link, depth):
        self._logger.debug("closing channels at depth = {}. has started topic channels = {}",
                           depth, self._has_started_topic_channels())
        self._bus_status = BusStatus.SHUTTING_DOWN
        while self._has_started_topic_channels():
            topic_channel = self._get_next_started_topic_channel()
            await topic_channel.stop()
        self._bus_status = BusStatus.STOPPED

    @property
    def is_bus_running(self):
        return self._bus_status is BusStatus.STARTED

    @property
    def is_bus_stopped(self):
        return self._bus_status is BusStatus.STOPPED
