from bbp.tag_script.parser.model.operator_enum import OperatorEnum
from bbp.tag_script.parser.binary_operator import BinaryOperator


class LogicalBinaryOperator(BinaryOperator):

    def _eval(self, frame):
        lhs_value = self.lhs.eval(frame)
        rhs_value = self.rhs.eval(frame)

        value = None
        if self.operator == OperatorEnum.LOGICAL_OR:
            value = lhs_value or rhs_value
        elif self.operator == OperatorEnum.LOGICAL_AND:
            value = lhs_value and rhs_value

        return value
