import unittest
from mock import patch

from bbpyp.ll_combinator.reserved import Reserved


@patch('test.TestContext', create=True)
class TestReserved(unittest.TestCase):

    def test_reserved_initialized_as_expected(self, test_context):
        expected_value = test_context.value
        expected_tag = test_context.tag

        parser = Reserved(test_context.tag, test_context.value, test_context.concat_factory,
                          test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertIs(expected_value, parser.value)
        self.assertIs(expected_tag, parser.tag)

    def test_reserved_string_representation_is_as_expected(self, test_context):
        expected_representation = f"{Reserved.__name__}({test_context.tag}, {test_context.value})"

        parser = Reserved(test_context.tag, test_context.value, test_context.concat_factory,
                          test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertEqual(expected_representation, f"{parser}")

    def test_reserved_call_with_none_matching_token_tag_returns_None(self, test_context):
        tokens = [("KEYWORD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        position = 0

        parser = Reserved("SYNTAX", "while", test_context.concat_factory,
                          test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        self.assertEqual(position, result.position)
        self.assertIsNone(result.value)

    def test_reserved_call_with_none_matching_token_value_returns_None(self, test_context):
        tokens = [("KEYWORD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        position = 0

        parser = Reserved("KEYWORD", "(", test_context.concat_factory,
                          test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        self.assertEqual(position, result.position)
        self.assertIsNone(result.value)

    def test_reserved_call_with_invalid_token_returns_None(self, test_context):
        tokens = [("KEYWORD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        position = 0

        parser = Reserved(test_context.invalid_token_tag, test_context.invalid_token_value,
                          test_context.concat_factory, test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        self.assertEqual(position, result.position)
        self.assertIsNone(result.value)

    def test_reserved_call_with_matching_token_returns_result_with_matched_token_value_and_position_incremented_by_1(self, test_context):
        expected_return_value = "("
        expected_return_position = 2
        tokens = [("KEYWORD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        position = 1

        parser = Reserved("SYNTAX", "(", test_context.concat_factory,
                          test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)
        self.assertEqual(expected_return_value, result.value)
        self.assertEqual(expected_return_position, result.position)

    def test_reserved_adding_two_reserved_parsers_should_produce_a_concatonation(self, test_context):
        reserved1 = Reserved("SYNTAX", "+", test_context.concat_factory,
                             test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        reserved2 = Reserved("SYNTAX", "+", test_context.concat_factory,
                             test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        parser = reserved1 + reserved2
