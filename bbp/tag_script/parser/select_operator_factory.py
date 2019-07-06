from bbp.tag_script.parser.model.operator_enum import OperatorEnum
from bbp.tag_script.parser.model.arity_enum import ArityEnum
from bbp.tag_script.parser.exception.tag_script_value_error import TagScriptValueError


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
            raise TagScriptValueError("operator", operator,
                                      f"must have an arity of {ArityEnum.ONE} or {ArityEnum.TWO}.")

        return factory(operator)
