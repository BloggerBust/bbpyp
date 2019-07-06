from bbp.tag_script.parser.model.operator_enum import OperatorEnum
from bbp.tag_script.parser.model.precedence_level_enum import PrecedenceLevelEnum


class BinaryOperatorFactory():
    def __init__(self, arethmatic_binary_operator_factory, relational_binary_operator_factory, logical_binary_operator_factory):
        self._arethmatic_binary_operator_factory = arethmatic_binary_operator_factory
        self._relational_binary_operator_factory = relational_binary_operator_factory
        self._logical_binary_operator_factory = logical_binary_operator_factory

    def __call__(self, operator):
        operator = OperatorEnum(operator)
        factory = None

        if operator.precedence < OperatorEnum("!").precedence:
            factory = self._logical_binary_operator_factory
        elif OperatorEnum("<").precedence <= operator.precedence <= OperatorEnum(">=").precedence:
            factory = self._relational_binary_operator_factory
        elif OperatorEnum("+").precedence <= operator.precedence <= OperatorEnum("/").precedence:
            factory = self._arethmatic_binary_operator_factory

        return factory(operator)
