class SinglyLinkedList:
    def __init__(self, single_link_node_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._linked_node_factory = single_link_node_factory
        self._header = self._linked_node_factory()
        self._tail = None

    def __iter__(self):
        return iter(self.head)

    def __repr__(self):
        return f"{self.__module__}.{self.__class__.__name__}()"

    def __str__(self):
        return self.__repr__()

    def append(self, value=None):
        self.insert(value)

    def insert(self, value=None, link_before=None):
        if link_before is not None:
            link_after = link_before.next_link
            link_before.next_link = self._linked_node_factory(value, link_after)
        elif self.is_empty:
            self._header.next_link = self._linked_node_factory(value)
            self._tail = self._header.next_link
        else:
            old_tail = self._tail
            old_tail.next_link = self._linked_node_factory(value)
            self._tail = old_tail.next_link

    def find(self, value):
        if self.is_empty:
            return None

        current_link = self.head
        while current_link is not None:
            if current_link.value == value:
                break
            current_link = current_link.next_link

        return current_link

    @property
    def head(self):
        return self._header.next_link

    @property
    def tail(self):
        return self._tail

    @property
    def is_empty(self):
        return self.head is None
