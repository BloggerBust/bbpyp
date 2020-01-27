from bbpyp.lexicomb.parser.binary_operator import BinaryOperator
from bbpyp.lexicomb.parser.model.operator_enum import OperatorEnum


class RelationalBinaryOperator(BinaryOperator):

    def __repr__(self):
        return f"({self.operator.name} {self.lhs} {self.rhs})"

    def _eval(self, frame):
        lhs_value = self.lhs.eval(frame)
        rhs_value = self.rhs.eval(frame)
        value = None
        if self.operator is OperatorEnum.RELATIONAL_LT:
            value = lhs_value < rhs_value
        elif self.operator is OperatorEnum.RELATIONAL_LT_OR_EQ:
            value = lhs_value <= rhs_value
        elif self.operator is OperatorEnum.RELATIONAL_EQ:
            value = lhs_value == rhs_value
        elif self.operator is OperatorEnum.RELATIONAL_GT_OR_EQ:
            value = lhs_value >= rhs_value
        elif self.operator is OperatorEnum.RELATIONAL_GT:
            value = lhs_value > rhs_value
        elif self.operator is OperatorEnum.RELATIONAL_NOT_EQ:
            value = lhs_value != rhs_value

        return value
