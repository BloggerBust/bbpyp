from bbpyp.lexicomb.parser.model.operator_enum import OperatorEnum
from bbpyp.lexicomb.parser.model.arity_enum import ArityEnum
from bbpyp.lexicomb.parser.exception.lexicomb_value_error import LexicombValueError


class SelectOperatorFactory():
    def __init__(self, unary_operator_factory, binary_operator_factory):
        self._unary_operator_factory = unary_operator_factory
        self._binary_operator_factory = binary_operator_factory

    def __call__(self, operator):
        operator_enum = OperatorEnum(operator)

        factory = None
        if operator_enum.arity == ArityEnum.TWO:
            factory = self._binary_operator_factory
        elif operator_enum.arity == ArityEnum.ONE:
            factory = self._unary_operator_factory
        else:
            raise LexicombValueError("operator", operator,
                                     f"must have an arity of {ArityEnum.ONE} or {ArityEnum.TWO}.")

        return factory(operator)
