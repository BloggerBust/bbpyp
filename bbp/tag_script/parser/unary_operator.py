from bbp.tag_script.parser.artifact import Artifact


class UnaryOperator(Artifact):

    def __init__(self, operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._operator = operator
        self._operand = None

    def __call__(self, operand):
        assert self._operand is None
        self._operand = operand

        return self

    def __repr__(self):
        return f"{type(self).__name__}({self.operator}, {self.operand})"

    @property
    def operator(self):
        return self._operator

    @property
    def operand(self):
        return self._operand
