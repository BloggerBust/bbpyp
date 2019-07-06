class PubSub:

    def __init__(self, logger, linked_list, bus_factory, async_service, context_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logger
        self._logger.debug(
            f"PubSub: context_service = {context_service}")
        self.__daisy_chain_bus = linked_list
        self.__bus_factory = bus_factory
        self._async_service = async_service
        self._context_service = context_service

        self.__daisy_chain_bus.append(self.__bus_factory())

    def register_topic_publisher(self, topic, publisher, **kwargs):
        self.__head_bus.register_topic_publisher(topic, publisher, **kwargs)

    def register_topic_subscriber(self, topic, subscriber, **kwargs):
        self.__head_bus.register_topic_subscriber(topic, subscriber, **kwargs)

    def register_message_pipeline(self, pipe_line):
        message_bus_link = self.__daisy_chain_bus.head
        for message_pipe_node in pipe_line:
            if message_bus_link is None:
                message_bus = self.__bus_factory()
                self.__daisy_chain_bus.append(message_bus)
                message_bus_link = self.__daisy_chain_bus.tail

            message_bus = message_bus_link.value
            message_bus_link = message_bus_link.next_link

            message_pipe = message_pipe_node.value
            topic = message_pipe.topic
            for publisher in message_pipe.sources:
                message_bus.register_topic_publisher(topic, publisher)
            for subscriber, kwargs in message_pipe.destinations:
                message_bus.register_topic_subscriber(topic, subscriber, **kwargs)

    def start(self):
        self._logger.info("Starting the pub sub service.")
        self._async_service.run(self.__start)
        self._logger.info("The Pub Sub service has shutdown")

    async def __start(self):
        next_bus_link = self.__daisy_chain_bus.head.next_link
        async with self._async_service.create_channel_context() as channel_context:
            self._logger.debug("starting the head message bus")
            channel_context.start_soon(self.__head_bus.start_bus, next_bus_link)

    @property
    def __head_bus(self):
        return self.__daisy_chain_bus.head.value
