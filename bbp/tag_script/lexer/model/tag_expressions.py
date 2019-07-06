import re

from bbp.tag_script.lexer.error.tag_expression_value_error import TagExpressionValueError
from bbp.common.model.deeply_copyable import DeeplyCopyable


class TagExpressions(DeeplyCopyable):
    def __init__(self, tag, expressions):
        if not tag is None and not isinstance(tag, str):
            raise TagExpressionValueError("tag", tag, "must be a string or None")

        if not tag is None and not re.search(r"^[a-zA-Z_]\w*$", tag, re.ASCII):
            raise TagExpressionValueError(
                "tag", tag, "must be alpha numeric, begin with a letter and may contain underscores")

        if not isinstance(expressions, list):
            raise TagExpressionValueError("expressions", expressions, "must be a list")

        self._tag = tag
        self._expressions = list()

        for expression in expressions:
            try:
                self._expressions.append(re.compile(expression))
            except Exception as error:
                raise TagExpressionValueError(
                    "expression", expression, f"must be a valid regular expression pattern", inner_exception=error)

    @property
    def tag(self):
        return self._tag

    @property
    def expressions(self):
        return self._expressions
