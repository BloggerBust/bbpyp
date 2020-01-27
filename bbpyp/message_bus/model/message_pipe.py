from bbpyp.message_bus.exception.message_bus_value_error import MessageBusValueError


class MessagePipe:
    def __init__(self, topic, sources=[], destinations=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(sources, list):
            raise MessageBusValueError("sources", sources, f"Sources must be a list.")

        if not isinstance(destinations, list):
            raise MessageBusValueError("destinations", destinations,
                                       f"Destinations must be a list.")

        self._topic = topic
        self._sources = sources
        self._destinations = destinations

    def __repr__(self):
        return f"{self.__module__}.{self.__class__.__name__}({self.topic}, {self.sources}, {self.destinations})"

    @property
    def topic(self):
        return self._topic

    @property
    def sources(self):
        return self._sources

    @property
    def destinations(self):
        return self._destinations
