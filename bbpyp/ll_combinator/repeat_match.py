from bbpyp.ll_combinator.model.result import Result
from bbpyp.abstract_parser.operand_combinator import OperandCombinator


class RepeatMatch(OperandCombinator):
    def __init__(self, parser, match_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parser = match_factory(parser)

    def __repr__(self):
        return f"{type(self).__name__}({self.parser.parser})"

    def __call__(self, tokens, position):

        matches = []
        result = self.parser(tokens, position)
        while result.value:
            matches.append(result.value)
            result = self.parser(tokens, result.position)
        if not len(matches) and result.value is not None:
            matches.append(result.value)

        return Result(matches, result.position)

    @property
    def parser(self):
        return self._parser
