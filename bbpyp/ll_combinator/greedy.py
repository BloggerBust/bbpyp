from bbpyp.ll_combinator.model.result import Result
from bbpyp.abstract_parser.operand_combinator import OperandCombinator


class Greedy(OperandCombinator):
    def __init__(self, parser, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parser = parser

    def __repr__(self):
        return f"{type(self).__name__}({self.parser})"

    def __call__(self, tokens, position):

        result = self.parser(tokens, position)
        if result.value is not None and result.position != len(tokens):
            return Result(None, position)
        return result

    @property
    def parser(self):
        return self._parser
