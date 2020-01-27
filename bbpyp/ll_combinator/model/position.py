class Position:
    def __init__(self, line, column):
        self._line = line
        self._column = column

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, line):
        self._line = line

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, column):
        self._column = column

    def __repr__(self):
        return f"{type(self).__name__}({self.line}, {self.column})"
