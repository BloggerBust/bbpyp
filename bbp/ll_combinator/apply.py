from bbp.abstract_parser.binary_operator_combinator import BinaryOperatorCombinator


class Apply(BinaryOperatorCombinator):

    def __repr__(self):
        return f"{type(self).__name__}({self.parser}, {self.function})"

    def __call__(self, tokens, position):
        result = self.parser(tokens, position)
        if result.value:
            result.value = self.function(result.value)
        return result

    @property
    def parser(self):
        return self.lhs_parser

    @property
    def function(self):
        return self.rhs_parser
