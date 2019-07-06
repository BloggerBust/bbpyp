import re
from bbp.tag_script.lexer.error.tag_expression_value_error import TagExpressionValueError


class TagExpressionsBuilder:
    def __init__(self, tag_expressions_factory):
        self._tag_expressions_factory = tag_expressions_factory
        self._tag = None
        self._expressions = []
        self._tag_expressions = []

    def with_tag(self, tag):
        if(not tag is None and not isinstance(tag, str)):
            raise TagExpressionValueError("tag", tag, "must be a string")

        self._tag = tag
        return self

    def with_expression(self, expression):
        if(not isinstance(expression, str)):
            raise TagExpressionValueError("expression", expression, "must be a string")

        self._expressions.append(expression)
        return self

    def with_expressions(self, expressions):
        if(not isinstance(expressions, list)):
            raise TagExpressionValueError("expressions", expressions, "must be a list")

        for expression in expressions:
            self.with_expression(expression)

        return self

    def append(self):
        self._tag_expressions.append(self._tag_expressions_factory(self._tag, self._expressions))
        self._tag = None
        self._expressions = []
        return self

    def build(self):
        if len(self._expressions):
            self.append()

        copy = self._tag_expressions.copy()
        return [(tag_expressions.tag,  tag_expressions.expressions) for tag_expressions in copy]
