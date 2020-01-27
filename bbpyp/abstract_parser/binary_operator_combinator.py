from bbpyp.abstract_parser.parser import Parser


class BinaryOperatorCombinator(Parser):
    def __init__(self, lhs, rhs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._lhs_parser = lhs
        self._rhs_parser = rhs

    @property
    def lhs_parser(self):
        return self._lhs_parser

    @property
    def rhs_parser(self):
        return self._rhs_parser
