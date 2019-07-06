import unittest
from mock import patch, create_autospec

from bbp.ll_combinator.greedy import Greedy


@patch('test.TestContext', create=True)
class TestGreedy(unittest.TestCase):

    def test_greedy_initialized_as_expected(self, test_context):
        expected_parser = test_context.parser

        parser = Greedy(test_context.parser, test_context.concat_factory,
                        test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertIs(expected_parser, parser.parser)

    def test_greedy_string_representation_is_as_expected(self, test_context):
        expected_representation = f"{Greedy.__name__}({test_context.parser})"

        parser = Greedy(test_context.parser, test_context.concat_factory,
                        test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertEqual(expected_representation, f"{parser}")

    @patch("bbp.ll_combinator.model.result.Result", value=None, autospec=True)
    def test_greedy_call_with_no_match_returns_none(self, mock_result, test_context):

        test_context.parser.return_value = mock_result

        tokens = [("Int", "x"), ("SYNTAX", "+"), ("SYNTAX", "+")]
        position = 0

        parser = Greedy(test_context.parser, test_context.concat_factory,
                        test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        test_context.parser.assert_called_once_with(tokens, position)
        self.assertEqual(mock_result, result)
        self.assertIsNone(result.value)

    @patch("bbp.ll_combinator.model.result.Result", position=1, autospec=True)
    def test_greedy_call_with_match_returns_none_if_tokens_remain(self, mock_result, test_context):
        test_context.parser.return_value = mock_result

        tokens = [("Int", "x"), ("SYNTAX", "+"), ("SYNTAX", "+")]
        position = 0

        parser = Greedy(test_context.parser, test_context.concat_factory,
                        test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        test_context.parser.assert_called_once_with(tokens, position)
        self.assertIsNone(result.value)

    @patch("bbp.ll_combinator.model.result.Result", autospec=True)
    def test_greedy_call_with_match_returns_expected_result_if_no_tokens_remain(self, mock_result, test_context):

        tokens = [("Int", "x"), ("SYNTAX", "+"), ("SYNTAX", "+")]
        position = 0
        mock_result.position = len(tokens)
        test_context.parser.return_value = mock_result

        parser = Greedy(test_context.parser, test_context.concat_factory,
                        test_context.lhs_or_rhs_factory, test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        test_context.parser.assert_called_once_with(tokens, position)

        self.assertIsNotNone(result.value)
        self.assertEqual(result, mock_result)
