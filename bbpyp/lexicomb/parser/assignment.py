from bbpyp.lexicomb.parser.statement import Statement


class Assignment(Statement):
    def __init__(self, destination, source, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._destination = destination
        self._source = source

    def __repr__(self):
        return f"{self.artifact_name}({self._destination}, {self._source})"

    def _eval(self, frame):
        source_value = self._source.eval(frame)
        result = self._destination(frame, source_value)
        return result
