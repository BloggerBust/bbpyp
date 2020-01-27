from bbpyp.lexicomb.parser.binary_operator import BinaryOperator
from bbpyp.lexicomb.parser.model.operator_enum import OperatorEnum


class ArethmaticBinaryOperator(BinaryOperator):
    BLANK_SPACE_SENTINEL = None

    def __init__(self, operator, real_number_factory, string_factory, *args, **kwargs):
        super().__init__(operator, *args, **kwargs)
        self._real_number_factory = real_number_factory
        self._string_factory = string_factory

    def __repr__(self):
        return f"({self.operator} {self.lhs} {self.rhs})"

    def _eval(self, frame):
        lhs_value = self.lhs.eval(frame)
        rhs_value = self.rhs.eval(frame)

        value = None
        if self.operator.value == OperatorEnum.ARETHMATIC_ADDITION.value:

            try:
                lhs_value = " " if lhs_value == ArethmaticBinaryOperator.BLANK_SPACE_SENTINEL else lhs_value
                rhs_value = " " if rhs_value == ArethmaticBinaryOperator.BLANK_SPACE_SENTINEL else rhs_value

                value = lhs_value + rhs_value
            except TypeError:
                value = f"{lhs_value}{rhs_value}"

        elif self.operator.value == OperatorEnum.ARETHMATIC_SUBTRACTION.value:
            value = lhs_value - rhs_value
        elif self.operator.value == OperatorEnum.ARETHMATIC_MULTIPLICATION.value:
            value = lhs_value * rhs_value
        elif self.operator.value == OperatorEnum.ARETHMATIC_DIVISION.value:
            value = lhs_value / rhs_value

        try:
            return self._real_number_factory(value).eval(frame)
        except ValueError:
            return self._string_factory(value).eval(frame)
