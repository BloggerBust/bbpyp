from bbpyp.abstract_parser.operand_combinator import OperandCombinator


class Match(OperandCombinator):

    def __init__(self, parser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parser = parser

    def __repr__(self):
        return f"{type(self).__name__}({self.parser})"

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        self.update_parse_progress(tokens, result.position)

        return result

    @property
    def parser(self):
        return self._parser
