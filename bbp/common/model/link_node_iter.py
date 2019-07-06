class LinkNodeIter:
    def __init__(self, link):
        self._link = link

    def __iter__(self):
        return self

    def __next__(self):
        next_value = self._link
        if next_value is not None:
            self._link = next_value.next_link
        else:
            raise StopIteration

        return next_value
