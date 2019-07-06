from abc import abstractmethod

from bbp.message_bus.bus_participant import BusParticipant


class AbstractPublisher(BusParticipant):
    __PUBLISHER_CONNECTION_KEY = "PUBLISHER_CONNECTION_KEY"

    async def connect_publisher(self, send_channel, kwargs):
        self._logger.debug("connect_publisher for topic {} with kwargs {}", self.topic, kwargs)
        self.__send_channel = send_channel
        async with self.__send_channel:
            self._logger.debug("started publishing to {}, send_channel statistics: {}",
                               self.topic, self.__send_channel.statistics())

            await self._before_publication()
            await self._begin_publication()
            await self._after_publication()

            statistics = self.__send_channel.statistics()
            self._logger.debug(
                f"from connect_publisher, after begin_publication: statistics = {statistics}")
            self.__disconnect_publisher(statistics)

        self._logger.debug(
            f"ended publishing to {self.topic}")

    def __disconnect_publisher(self, statistics):
        self.disconnect_event.set()
        self._logger.debug(
            "disconnecting publication to topic {} using event [{}], receive_channel statistics: {}", self.topic, self.disconnect_event, statistics)
        self._publisher_has_disconnected()

    @abstractmethod
    def _publisher_has_disconnected(self):
        pass

    @abstractmethod
    async def _before_publication(self, *args, **kwargs):
        pass

    @abstractmethod
    async def _begin_publication(self):
        raise NotImplementedError("must override abstractmethod: _begin_publication")

    @abstractmethod
    async def _after_publication(self):
        pass

    async def publish_message(self, message):
        was_waiting = False
        if not self.connect_event.is_set():
            self._logger.debug(
                "The publisher is waiting for itself to connect with event [{}]...", self.connect_event)
            was_waiting = True
        await self.connect_event.wait()
        if was_waiting:
            self._logger.debug("The publisher received connect event [{}]", self.connect_event)

        await self.__send_channel.send((self.topic, message))

    @property
    def __send_channel(self):
        return self._context_service.get_context_variable(type(self).__PUBLISHER_CONNECTION_KEY)

    @__send_channel.setter
    def __send_channel(self, send_channel):
        self._context_service.set_context_variable(
            type(self).__PUBLISHER_CONNECTION_KEY, send_channel)
        self.connect_event.set()
        self._logger.debug("publisher connect event [{}] has been set", self.connect_event)
