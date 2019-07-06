from bbp.abstract_parser.parser import Parser


class OperandCombinator(Parser):

    def __init__(self, concat_factory, lhs_or_rhs_factory, expression_factory, apply_factory, greedy_factory, defer_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._concat_factory = concat_factory
        self._lhs_or_rhs_factory = lhs_or_rhs_factory
        self._expression_factory = expression_factory
        self._apply_factory = apply_factory
        self._greedy_factory = greedy_factory
        self._defer_factory = defer_factory

    def __repr__(self):
        return f"{type(self).__name__}()"

    def __add__(self, rhs):
        return self._defer_factory(lambda: self._concat_factory(self, rhs))

    def __or__(self, rhs):
        return self._defer_factory(lambda: self._lhs_or_rhs_factory(self, rhs))

    def __rshift__(self, rhs):
        return self._defer_factory(lambda: self._apply_factory(self, rhs))

    def __lshift__(self, rhs):
        return self._greedy_factory(self + rhs)

    def __mul__(self, rhs):
        return self._defer_factory(lambda: self._expression_factory(self, rhs))

    def __matmul__(self, rhs):
        return self._defer_factory(lambda: rhs(self))
