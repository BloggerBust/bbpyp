from abc import abstractmethod
from bbp.message_bus.bus_participant import BusParticipant


class AbstractSubscriber(BusParticipant):

    async def connect_subscriber(self, receive_channel, publisher_connect_event, publisher_disconnect_event, kwargs):
        self._logger.debug("connect_subscriber for topic {} with kwargs {}", self.topic, kwargs)
        self.connect_event.set()
        self._logger.debug(
            "connect_subscriber: set subscriber_connect_event [{}]", self.connect_event)
        if not publisher_connect_event.is_set():
            self._logger.debug(
                "The subscriber is waiting for the publisher with publisher_connect_event = [{}] to connect...", publisher_connect_event)
        await publisher_connect_event.wait()
        async with receive_channel:
            statistics = receive_channel.statistics()
            self._logger.debug(
                "started subscriber to {}, receive_channel statistics: {}, publisher_disconnect_event = {}", self.topic, statistics, publisher_disconnect_event)

            await self._before_subscription(**kwargs)
            last_tasks_waiting_to_receive = -1
            last_tasks_waiting_to_send = -1
            while not publisher_disconnect_event.is_set() or statistics.tasks_waiting_send > 0 or statistics.tasks_waiting_receive > 0:
                async for topic, message in receive_channel:
                    assert topic == self.topic
                    await self._process_subscription_message(message)
                    statistics = receive_channel.statistics()
                await self._async_service.sleep()
                statistics = receive_channel.statistics()

            await self._after_subscription(**kwargs)
            statistics = receive_channel.statistics()
            await self.__disconnect_subscriber(statistics, **kwargs)

    async def __disconnect_subscriber(self, statistics, *args, **kwargs):
        self._logger.debug(
            "disconnecting subscription to topic {} using event [{}], receive_channel statistics: {}", self.topic, self.disconnect_event, statistics)
        self.disconnect_event.set()
        await self._on_disconnect_subscriber(*args, **kwargs)

    async def _before_subscription(self, *args, **kwargs):
        pass

    @abstractmethod
    async def _process_subscription_message(self, topic, message):
        raise NotImplementedError("must override abstractmethod: _process_subscription_message")

    async def _after_subscription(self, *args, **kwargs):
        self._logger.debug(
            "_after_subscription called for topic [{}] with args = {}, kwargs = {}", self.topic, args, kwargs)

    async def _on_disconnect_subscriber(self, *args, **kwargs):
        self._logger.debug(
            "_on_disconnect_subscriber called for topic [{}] with args = {}, kwargs = {}", self.topic, args, kwargs)
