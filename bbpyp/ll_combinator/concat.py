from bbpyp.abstract_parser.binary_operator_combinator import BinaryOperatorCombinator
from bbpyp.ll_combinator.model.result import Result


class Concat(BinaryOperatorCombinator):

    def __repr__(self):
        return f"{type(self).__name__}({self.lhs_parser}, {self.rhs_parser})"

    def __call__(self, tokens, position):
        lhs_result = self.lhs_parser(tokens, position)
        if lhs_result.value is not None:
            rhs_result = self.rhs_parser(tokens, lhs_result.position)
            if rhs_result.value is not None:
                combined_values = (lhs_result.value, rhs_result.value)
                return Result(combined_values, rhs_result.position)
        return Result(None, position)
