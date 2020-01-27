import unittest
from mock import patch

from bbpyp.ll_combinator.apply import Apply


@patch('test.TestContext', create=True)
class TestApply(unittest.TestCase):

    def test_apply_initialized_as_expected(self, test_context):
        expected_parser = test_context.parser
        expected_function = test_context.function

        parser = Apply(test_context.parser, test_context.function,
                       source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertIs(expected_parser, parser.parser)
        self.assertIs(expected_function, parser.function)

    def test_apply_string_representation_is_as_expected(self, test_context):
        expected_representation = f"{Apply.__name__}({test_context.parser}, {test_context.function})"

        parser = Apply(test_context.parser, test_context.function,
                       source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertEqual(expected_representation, f"{parser}")

    def test_apply_call_with_no_matching_tokens_returns_result_value_none(self, test_context):

        test_context.expected_result.value = None
        test_context.parser.return_value = test_context.expected_result
        tokens = [("KEYWORD", "int"), ("SYNTAX", "+"), ("SYNTAX", "+")]
        position = 0

        parser = Apply(test_context.parser, test_context.function,
                       source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        test_context.parser.assert_called_once_with(tokens, position)
        test_context.function.assert_not_called()
        self.assertIsNone(result.value)

    @patch('bbpyp.ll_combinator.model.result.Result', spec_set=True, autospec=True)
    def test_apply_call_with_matching_tokens_applies_function_to_result_value(self, mock_parse_result, test_context):

        expected_parse_result_value = mock_parse_result.value = 5
        expected_parse_result_position = mock_parse_result.position
        test_context.parser.return_value = mock_parse_result

        expected_function_result_value = test_context.function.return_value = mock_parse_result.value + 1

        tokens = [("Int", 5)]
        position = 0

        parser = Apply(test_context.parser, test_context.function,
                       source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        test_context.parser.assert_called_once_with(tokens, position)
        test_context.function.assert_called_once_with(expected_parse_result_value)
        self.assertEqual(result.value, expected_function_result_value)
        self.assertEqual(result.position, expected_parse_result_position)
