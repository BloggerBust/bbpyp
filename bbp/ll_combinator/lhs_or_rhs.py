from bbp.abstract_parser.binary_operator_combinator import BinaryOperatorCombinator


class LhsOrRhs(BinaryOperatorCombinator):

    def __repr__(self):
        return f"{type(self).__name__}({self.lhs_parser}, {self.rhs_parser})"

    def __call__(self, tokens, position):
        result = self.lhs_parser(tokens, position)
        if result.value is None:
            result = self.rhs_parser(tokens, position)

        return result
