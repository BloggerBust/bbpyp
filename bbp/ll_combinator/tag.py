from bbp.ll_combinator.model.result import Result
from bbp.ll_combinator.model.token_enum import TokenEnum
from bbp.abstract_parser.operand_combinator import OperandCombinator


class Tag(OperandCombinator):
    def __init__(self, tag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tag = tag

    def __call__(self, tokens, position):
        if(position < len(tokens)
           and tokens[position][TokenEnum.TAG] is self.tag):
            return Result(tokens[position][TokenEnum.VALUE], position + 1)
        return Result(None, position)

    @property
    def tag(self):
        return self._tag

    def __repr__(self):
        return f"{type(self).__name__}({self.tag})"
