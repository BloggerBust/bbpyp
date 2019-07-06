import unittest
from mock import patch, create_autospec, call

from bbp.ll_combinator.repeat_match import RepeatMatch


@patch('test.TestContext', create=True)
class TestRepeatMatch(unittest.TestCase):

    def test_repeat_match_initialized_as_expected(self, test_context):
        expected_parser = test_context.mock_match_factory.return_value

        parser = RepeatMatch(test_context.parser, test_context.mock_match_factory, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                             test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        test_context.mock_match_factory.assert_called_once_with(test_context.parser)
        self.assertIs(expected_parser, parser.parser)

    def test_repeat_match_string_representation_is_as_expected(self, test_context):
        test_context.mock_match_factory.return_value.parser = test_context.parser
        expected_representation = f"{RepeatMatch.__name__}({test_context.parser})"

        parser = RepeatMatch(test_context.parser, test_context.mock_match_factory, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                             test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertEqual(expected_representation, f"{parser}")

    @patch('bbp.ll_combinator.repeat_match.Result', autospec=True)
    def test_repeat_match_call_with_no_matching_tokens_returns_result_with_empty_list_value_and_position_unchanged(self, mock_result, test_context):

        mock_match_factory_result = create_autospec(mock_result.__class__, spec_set=True)
        mock_match_factory_result.return_value.value = None
        mock_match_factory_result.return_value.position = 1
        test_context.mock_match_factory.return_value = mock_match_factory_result

        expected_result_value = mock_result.return_value.value = []
        expected_result_position = mock_result.return_value.position = 1

        tokens = [("KEYWORD", "int"), ("SYNTAX", "+"), ("SYNTAX", "+")]
        position = 1

        parser = RepeatMatch(test_context.parser, test_context.mock_match_factory, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                             test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        test_context.mock_match_factory.assert_called_once_with(test_context.parser)

        result = parser(tokens, position)

        mock_match_factory_result.assert_called_once_with(tokens, position)
        mock_result.assert_called_once_with([], 1)

        self.assertIs(result, mock_result.return_value)
        self.assertIs(result.value, expected_result_value)
        self.assertIs(result.position, expected_result_position)

    @patch('bbp.ll_combinator.repeat_match.Result', autospec=True)
    def test_repeat_match_call_with_matching_tokens_returns_result_with_list_of_match_values_and_position_set_to_last_match_result_position(self, mock_result, test_context):

        tokens = [("KEYWORD", "int"), ("SYNTAX", "+"), ("SYNTAX", "+")]
        position = 1

        mock_match_factory_result1 = create_autospec(mock_result.__class__, spec_set=True)
        mock_match_factory_result1.value = "+"
        mock_match_factory_result1.position = 2

        mock_match_factory_result2 = create_autospec(mock_result.__class__, spec_set=True)
        mock_match_factory_result2.value = "+"
        mock_match_factory_result2.position = 3

        mock_match_factory_result3 = create_autospec(mock_result.__class__, spec_set=True)
        mock_match_factory_result3.value = None
        mock_match_factory_result3.position = 3

        test_context.parser.side_effect = [
            mock_match_factory_result1, mock_match_factory_result2, mock_match_factory_result3]
        test_context.mock_match_factory.return_value = test_context.parser

        expected_result_value = mock_result.return_value.value = ["+", "+"]
        expected_result_position = mock_result.return_value.position = 3
        expected_calls = [call(tokens, position), call(
            tokens, position + 1), call(tokens, position + 2)]

        test_context.mock_match_factory.return_value.parser = test_context.parser

        parser = RepeatMatch(test_context.parser, test_context.mock_match_factory, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                             test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        test_context.mock_match_factory.assert_called_once_with(test_context.parser)

        result = parser(tokens, position)

        self.assertEqual(test_context.parser.mock_calls, expected_calls)
        mock_result.assert_called_once_with(["+", "+"], position + 2)

        self.assertIs(result, mock_result.return_value)
        self.assertIs(result.value, expected_result_value)
        self.assertIs(result.position, expected_result_position)
