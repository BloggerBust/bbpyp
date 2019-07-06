from bbp.abstract_parser.operand_combinator import OperandCombinator


class Defer(OperandCombinator):
    def __init__(self, parser_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parser_factory = parser_factory
        self._parser = None

    def __repr__(self):
        return f"{type(self).__name__}({self._parser_factory})"

    def __call__(self, tokens, position):
        return self.parser(tokens, position)

    @property
    def parser(self):
        self._parser = self._parser_factory() if self._parser is None else self._parser
        return self._parser
