from bbp.tag_script.parser.model.operator_enum import OperatorEnum
from bbp.tag_script.parser.model.precedence_level_enum import PrecedenceLevelEnum


class UnaryOperatorFactory():
    def __init__(self, logical_unary_operator_factory, arethmatic_unary_operator_factory):
        self._logical_unary_operator_factory = logical_unary_operator_factory
        self._arethmatic_unary_operator_factory = arethmatic_unary_operator_factory

    def __call__(self, operator):
        operator = OperatorEnum(operator)
        factory = None

        if operator is OperatorEnum.LOGICAL_NEGATION:
            factory = self._logical_unary_operator_factory
        if operator is OperatorEnum.ARETHMATIC_NEGATIVE:
            factory = self._arethmatic_unary_operator_factory

        return factory(operator)
