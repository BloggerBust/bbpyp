import unittest
import re
from mock import patch, sentinel, Mock

from bbp.tag_script.lexer.tag_expressions_builder import TagExpressionsBuilder
from bbp.tag_script.lexer.error.tag_expression_value_error import TagExpressionValueError


@patch('test.TestContext', tag=str(), expression=str(), expressions=[], create=True)
class TestTagExpressionsBuilder(unittest.TestCase):

    def test_tag_expressions_builder_construction_initializes_as_expected(self, test_context):
        expected_tag_expressions_factory = test_context.tag_expressions_factory

        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        self.assertIs(builder._tag_expressions_factory, expected_tag_expressions_factory)
        self.assertEqual(builder._tag, None)
        self.assertEqual(builder._expressions, [])
        self.assertEqual(builder._tag_expressions, [])

    def test_tag_expressions_builder_with_tag_returns_self(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        self.assertIsInstance(builder.with_tag(test_context.tag), TagExpressionsBuilder)

    def test_tag_expressions_builder_with_expression_returns_self(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        self.assertIsInstance(builder.with_expression(
            test_context.expression), TagExpressionsBuilder)

    def test_tag_expressions_builder_with_expressions_returns_self(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        self.assertIsInstance(builder.with_expressions(
            test_context.expressions), TagExpressionsBuilder)

    def test_tag_expressions_builder_append_returns_self(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        self.assertIsInstance(builder.append(), TagExpressionsBuilder)

    def test_tag_expressions_builder_with_tag_overrides_existing_tag(self, test_context):
        expected_tag = "new tag"
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)
        builder._tag = test_context.tag

        builder.with_tag(expected_tag)

        self.assertIs(builder._tag, expected_tag)

    def test_tag_expressions_builder_with_tag_raises_tag_expression_value_error_when_tag_is_invalid(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        with self.assertRaisesRegex(TagExpressionValueError, re.escape(f"TagExpressionValueError: tag={test_context.bad_tag}: must be a string")):
            builder.with_tag(test_context.bad_tag)

    def test_tag_expressions_builder_with_expression_raises_tag_expression_value_error_when_expression_is_invalid(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        with self.assertRaisesRegex(TagExpressionValueError, re.escape(f"TagExpressionValueError: expression={test_context.bad_expression}: must be a string")):
            builder.with_expression(test_context.bad_expression)

    def test_tag_expressions_builder_with_expression_increments_length_of_expressions(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        for original_length in range(0, 3):
            self.assertEqual(len(builder._expressions), original_length)
            expected_length = original_length + 1

            builder.with_expression(test_context.expression)

            self.assertEqual(len(builder._expressions), expected_length)

    def test_tag_expressions_builder_with_expression_append_expected_expressions(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        for index in range(0, 3):
            expected_expression = str(sentinel.expression)
            builder.with_expression(expected_expression)

            self.assertIs(builder._expressions[index], expected_expression)

    def test_tag_expressions_builder_with_expressions_raises_tag_expression_value_error_when_expression_is_invalid(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        with self.assertRaisesRegex(TagExpressionValueError, re.escape(f"TagExpressionValueError: expressions={test_context.bad_expressions}: must be a list")):
            builder.with_expressions(test_context.bad_expressions)

    def test_tag_expressions_builder_with_expressions_calls_with_expression_for_each_expression_in_list(self, test_context):
        cases = [
            ([], 0),
            ([""], 1),
            (["", "", ""], 3)
        ]

        for provided, expected_call_count in cases:
            with test_context.mock_with_expression as mock_with_expression:
                builder = TagExpressionsBuilder(test_context.tag_expressions_factory)
                builder.with_expression = mock_with_expression
                builder.with_expressions(provided)
                self.assertEqual(expected_call_count, mock_with_expression.call_count)
                mock_with_expression.reset_mock()

    def test_tag_expressions_builder_append_increases_length_of_tag_expressions(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)

        for original_length in range(0, 3):
            self.assertEqual(len(builder._tag_expressions), original_length)
            expected_length = original_length + 1

            builder.append()

            self.assertEqual(len(builder._tag_expressions), expected_length)

    def test_tag_expressions_builder_append_resets_tag_and_expressions(self, test_context):
        builder = TagExpressionsBuilder(test_context.tag_expressions_factory)
        builder._tag = test_context.tag
        builder._expressions = test_context._expressions
        expected_tag = None
        expected_expressions = []

        builder.append()

        self.assertEqual(builder._tag, expected_tag)
        self.assertEqual(builder._expressions, expected_expressions)

    @patch("bbp.tag_script.lexer.model.tag_expressions.TagExpressions", autospec=True)
    def test_tag_expressions_builder_append_appends_a_tag_expressions_object_containing_tag_and_expressions(self, tag_expressions_factory, test_context):

        expected_tag = test_context.tag
        expected_expressions = test_context.expressions

        tag_expressions_factory.return_value.tag = test_context.tag
        tag_expressions_factory.return_value.expressions = test_context.expressions

        builder = TagExpressionsBuilder(tag_expressions_factory)
        builder._tag = test_context.tag
        builder._expressions = test_context.expressions

        builder.append()

        actual_tag_expressions = builder._tag_expressions[0]
        self.assertEqual(actual_tag_expressions.tag, expected_tag)
        self.assertEqual(actual_tag_expressions.expressions, expected_expressions)

    @patch("bbp.tag_script.lexer.model.tag_expressions.TagExpressions", autospec=True)
    def test_tag_expressions_builder_build_returns_tag_expressions(self, tag_expressions_factory, test_context):

        expected_tag = test_context.tag
        expected_expressions = [
            re.compile(expression) for expression in [r"/w*", r".*", r"[a-z]+"]]
        tag_expressions_factory.return_value.tag = test_context.tag
        tag_expressions_factory.return_value.expressions = expected_expressions
        expected_tag_expressions = [(expected_tag, expected_expressions)]

        mock_tag_expression = tag_expressions_factory(str(), [])

        builder = TagExpressionsBuilder(tag_expressions_factory)
        builder._tag_expressions = [mock_tag_expression]

        actual = builder.build()

        self.assertEqual(actual, [(test_context.tag, expected_expressions)])

    @patch("bbp.tag_script.lexer.model.tag_expressions.TagExpressions", autospec=True)
    def test_tag_expressions_builder_build_appends_dangling_tag_expressions(self, tag_expressions_factory, test_context):

        dangling_tag = "DANGLING"
        dangling_expressions = [r"/w*", r".*", r"[a-z]+"]
        dangling_compiled_expressions = [
            re.compile(expression) for expression in dangling_expressions]

        tag_expressions_factory.return_value.tag = dangling_tag
        tag_expressions_factory.return_value.expressions = dangling_compiled_expressions

        pre_appended_tag_expressions = [
            Mock(tag=None, expressions=[re.compile(r"\s*")]), Mock(tag="THING", expressions=[
                re.compile(r"[a-zA-Z0-9]"), re.compile(r"THING")])]

        expected_tag_expressions = [(pre_appended_tag_expression.tag, pre_appended_tag_expression.expressions)
                                    for pre_appended_tag_expression in pre_appended_tag_expressions] + [(dangling_tag, dangling_compiled_expressions)]

        builder = TagExpressionsBuilder(tag_expressions_factory)
        builder._expressions = dangling_expressions
        builder._tag = dangling_tag
        builder._tag_expressions = pre_appended_tag_expressions

        actual = builder.build()

        self.assertEqual(actual, expected_tag_expressions)
