import unittest
from mock import patch, create_autospec

from bbp.ll_combinator.concat import Concat


@patch('test.TestContext', create=True)
class TestConcat(unittest.TestCase):

    def test_concat_initialized_as_expected(self, test_context):
        expected_lhs_parser = test_context.lhs
        expected_rhs_parser = test_context.rhs

        parser = Concat(test_context.lhs, test_context.rhs,
                        source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertIs(expected_lhs_parser, parser.lhs_parser)
        self.assertIs(expected_rhs_parser, parser.rhs_parser)

    def test_concat_string_representation_is_as_expected(self, test_context):
        expected_representation = f"{Concat.__name__}({test_context.lhs}, {test_context.rhs})"

        parser = Concat(test_context.lhs, test_context.rhs,
                        source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertEqual(expected_representation, f"{parser}")

    @patch('bbp.ll_combinator.concat.Result', autospec=True)
    @patch('bbp.ll_combinator.concat.Result', value=None, autospec=True)
    def test_concat_call_with_lhs_not_matching_token_returns_result_constructed_with_value_None(self, lhs_result, rhs_result, test_context):
        test_context.lhs.return_value = lhs_result
        test_context.rhs.return_value = rhs_result
        tokens = [("KEYWORD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        start_position = 0

        parser = Concat(test_context.lhs, test_context.rhs,
                        source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, start_position)

        test_context.lhs.assert_called_once_with(tokens, start_position)
        test_context.rhs.assert_not_called()
        result.called_once_with(None, start_position)

    @patch('bbp.ll_combinator.concat.Result', value=None, autospec=True)
    @patch('bbp.ll_combinator.concat.Result', position=2, autospec=True)
    def test_concat_call_with_lhs_matching_token_and_rhs_not_matching_token_returns_result_constructed_with_value_None(self, lhs_result, rhs_result, test_context):
        start_position = 0
        test_context.lhs.return_value = lhs_result
        test_context.rhs.return_value = rhs_result
        tokens = [("KEYWORD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]

        parser = Concat(test_context.lhs, test_context.rhs,
                        source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, start_position)

        test_context.lhs.assert_called_once_with(tokens, start_position)
        test_context.rhs.assert_called_once_with(tokens, test_context.lhs.return_value.position)
        result.called_once_with(None, start_position)

    @patch('bbp.ll_combinator.concat.Result', position=2, value="rhs", autospec=True)
    @patch('bbp.ll_combinator.concat.Result', position=1, value="lhs", autospec=True)
    def test_concat_call_with_lhs_matching_token_and_rhs_matching_token_returns_expected_result(self, lhs_result, rhs_result, test_context):
        tokens = [("KEYWORD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        start_position = 0
        test_context.lhs.return_value = lhs_result
        test_context.rhs.return_value = rhs_result

        expected_result_value = (test_context.lhs.return_value.value,
                                 test_context.rhs.return_value.value)
        expected_result_position = test_context.rhs.return_value.position

        parser = Concat(test_context.lhs, test_context.rhs,
                        source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        result = parser(tokens, start_position)

        test_context.lhs.assert_called_once_with(tokens, start_position)
        test_context.rhs.assert_called_once_with(tokens, test_context.lhs.return_value.position)
        result.called_once_with(expected_result_value, expected_result_position)
