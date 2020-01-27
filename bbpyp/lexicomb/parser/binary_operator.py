from bbpyp.lexicomb.parser.artifact import Artifact


class BinaryOperator(Artifact):

    def __init__(self, operator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._operator = operator
        self._lhs = None
        self._rhs = None

    def __repr__(self):
        return f"({self.operator}, {self.lhs}, {self.rhs})"

    def __call__(self, lhs, rhs):
        assert self._lhs is None
        assert self._rhs is None
        self._lhs = lhs
        self._rhs = rhs

        return self

    @property
    def lhs(self):
        return self._lhs

    @property
    def rhs(self):
        return self._rhs

    @property
    def operator(self):
        return self._operator
