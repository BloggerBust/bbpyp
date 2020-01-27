import unittest
import re
from mock import patch

from bbpyp.lexicomb.lexer.model.tag_expressions import TagExpressions
from bbpyp.lexicomb.lexer.error.tag_expression_value_error import TagExpressionValueError


@patch("test.test_context", tag="VALID", expressions=["VALID"], create=True)
class TestTagExpressions(unittest.TestCase):
    def test_tag_expressions_with_invalid_tag_type_raises_tag_expression_value_error(self, test_context):

        none_exhausitve_list_of_invalid_types = [
            test_context.invalid_tag, dict(), list(), int(), float(), object(), tuple()]

        for invalid_type in none_exhausitve_list_of_invalid_types:
            with self.assertRaisesRegex(TagExpressionValueError, re.escape(f"TagExpressionValueError: tag={invalid_type}: must be a string or None")):
                TagExpressions(invalid_type, test_context.expressions)

    def test_tag_expressions_with_invalid_tag_raises_tag_expression_value_error(self, test_context):
        none_exhaustive_list_of_invalid_tags = ["", " ", "0", "!", "@", "#", "$", "%", "^", "&", "*",
                                                "(", ")", "{", "}", "[", "]", "-", "+", "=", "|", "\\", "/", " < ", ">", "?", "this is invalid"]

        for invalid_tag in none_exhaustive_list_of_invalid_tags:
            with self.assertRaisesRegex(TagExpressionValueError, re.escape(f"TagExpressionValueError: tag={invalid_tag}: must be alpha numeric, begin with a letter and may contain underscores"), msg=f"TagExpressionValueError not raised for tag [{invalid_tag}]"):
                TagExpressions(invalid_tag, test_context.expressions)

    def test_tag_expressions_with_valid_tag_sets_tag(self, test_context):
        valid_tags = [None, test_context.tag, "VALID_TAG", "_1234567890", "a1"]

        for expected_tag in valid_tags:
            tag_expression = TagExpressions(expected_tag, test_context.expressions)
            self.assertIs(tag_expression.tag, expected_tag)

    def test_tag_expressions_with_invalid_expression_type_raises_tag_expression_value_error(self, test_context):
        none_exhausitve_list_of_invalid_types = [
            test_context.invalid_expression, str(), dict(), int(), float(), object(), tuple(), None]

        for invalid_type in none_exhausitve_list_of_invalid_types:
            with self.assertRaisesRegex(TagExpressionValueError, re.escape(f"TagExpressionValueError: expressions={invalid_type}: must be a list"), msg=f"failed for type = {invalid_type}"):
                TagExpressions(test_context.tag, invalid_type)
            none_exhausitve_list_of_invalid_types.remove(invalid_type)

    def test_tag_expressions_with_invalid_expression_raises_tag_expression_value_error(self, test_context):
        none_exhausitve_list_of_invalid_expressions = ["[", "("]

        for invalid_pattern in none_exhausitve_list_of_invalid_expressions:
            with self.assertRaisesRegex(TagExpressionValueError, re.escape(f"TagExpressionValueError: expression={invalid_pattern}: must be a valid regular expression pattern"), msg=f"failed for invalid pattern = {invalid_pattern}"):
                TagExpressions(test_context.tag, none_exhausitve_list_of_invalid_expressions)
            none_exhausitve_list_of_invalid_expressions.remove(invalid_pattern)

    def test_tag_expressions_with_valid_expression_sets_expression(self, test_context):
        valid_expressions = test_context.expressions + \
            ["VALID EXPRESSION", "", r"^[a-zA-Z_]\w*$", "01 23, 456; 789"]

        tag_expressions = TagExpressions(test_context.tag, valid_expressions)
        index = 0
        for expression in tag_expressions.expressions:
            expected_expression = valid_expressions[index]
            self.assertIs(expression, re.compile(expected_expression))
            index = index + 1
