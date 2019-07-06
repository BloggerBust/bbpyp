from bbp.common.exception.bbp_value_error import BbpValueError


class SingleLinkNode:
    def __init__(self, value=None, next_link=None, link_node_iter_factory=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if next_link is not None and not isinstance(next_link, SingleLinkNode):
            raise BbpValueError("next_link", next_link,
                                f"Must be either None or of type {SingleLinkNode}")

        self._link_node_iter_factory = link_node_iter_factory
        self._value = value
        self._next_link = next_link

    def __iter__(self):
        return self._link_node_iter_factory(self)

    def __repr__(self):
        return f"{self.__module__}.{self.__class__.__name__}({self.value})"

    def __str__(self):
        return self.__repr__()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def next_link(self):
        return self._next_link

    @next_link.setter
    def next_link(self, next_link):
        self._next_link = next_link
