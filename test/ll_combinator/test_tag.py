import unittest
from mock import patch

from bbp.ll_combinator.tag import Tag


@patch('test.TestContext', create=True)
class TestTag(unittest.TestCase):

    def test_tag_initialized_as_expected(self, test_context):
        expected_tag = test_context.tag

        parser = Tag(test_context.tag, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                     test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertIs(expected_tag, parser.tag)

    def test_tag_string_representation_is_as_expected(self, test_context):
        expected_representation = f"{Tag.__name__}({test_context.tag})"

        parser = Tag(test_context.tag, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                     test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertEqual(expected_representation, f"{parser}")

    def test_tag_call_with_none_matching_token_tag_returns_None(self, test_context):
        tokens = [("KEYWORD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        position = 0

        parser = Tag(test_context.invalid_token, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                     test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        self.assertEqual(position, result.position)
        self.assertIsNone(result.value)

    def test_tag_call_with_matching_token_returns_result_with_matched_token_value_and_position_incremented_by_1(self, test_context):
        expected_return_value = "("
        expected_return_position = 2
        tokens = [("KEYWORD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        position = 1

        parser = Tag("SYNTAX", test_context.concat_factory, test_context.lhs_or_rhs_factory, test_context.expression_factory,
                     test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)
        self.assertEqual(expected_return_value, result.value)
        self.assertEqual(expected_return_position, result.position)
