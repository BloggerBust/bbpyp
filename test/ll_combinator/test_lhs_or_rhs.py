import unittest
from mock import patch

from bbp.ll_combinator.lhs_or_rhs import LhsOrRhs


@patch('test.TestContext', create=True)
class TestLhsOrRhs(unittest.TestCase):

    def test_lhs_or_rhs_initialized_as_expected(self, test_context):
        expected_lhs_parser = test_context.lhs
        expected_rhs_parser = test_context.rhs

        parser = LhsOrRhs(test_context.lhs, test_context.rhs,
                          source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertIs(expected_lhs_parser, parser.lhs_parser)
        self.assertIs(expected_rhs_parser, parser.rhs_parser)

    def test_lhs_or_rhs_string_representation_is_as_expected(self, test_context):
        expected_representation = f"{LhsOrRhs.__name__}({test_context.lhs}, {test_context.rhs})"

        parser = LhsOrRhs(test_context.lhs, test_context.rhs,
                          source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertEqual(expected_representation, f"{parser}")

    @patch("bbp.ll_combinator.model.result.Result", value=None, autospec=True)
    @patch("bbp.ll_combinator.model.result.Result", value=None, autospec=True)
    def test_lhs_or_rhs_call_with_none_matching_token_returns_None(self, mock_lhs_result, mock_rhs_result, test_context):
        test_context.lhs.return_value = mock_lhs_result
        test_context.rhs.return_value = mock_rhs_result
        tokens = [("KEYWLHS_OR_RHSD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        position = 0

        parser = LhsOrRhs(test_context.lhs, test_context.rhs,
                          source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        self.assertIs(result, mock_rhs_result)
        self.assertIsNone(result.value)

    @patch("bbp.ll_combinator.model.result.Result", value=None, autospec=True)
    @patch("bbp.ll_combinator.model.result.Result", autospec=True)
    def test_lhs_or_rhs_call_with_lhs_matching_token_returns_lhs_result(self, mock_lhs_result, mock_rhs_result, test_context):
        test_context.lhs.return_value = mock_lhs_result
        test_context.rhs.return_value = mock_rhs_result
        tokens = [("KEYWLHS_OR_RHSD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        position = 1

        parser = LhsOrRhs(test_context.lhs, test_context.rhs,
                          source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        test_context.lhs.assert_called_once_with(tokens, position)
        test_context.rhs.assert_not_called()
        self.assertIs(result, mock_lhs_result)

    @patch("bbp.ll_combinator.model.result.Result", autospec=True)
    @patch("bbp.ll_combinator.model.result.Result", position=1, value=None, autospec=True)
    def test_lhs_or_rhs_call_with_lhs_not_matching_token_and_rhs_matching_token_returns_rhs_result(self, mock_lhs_result, mock_rhs_result, test_context):
        test_context.lhs.return_value = mock_lhs_result
        test_context.rhs.return_value = mock_rhs_result
        tokens = [("KEYWLHS_OR_RHSD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        position = 0

        parser = LhsOrRhs(test_context.lhs, test_context.rhs,
                          source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        test_context.lhs.assert_called_once_with(tokens, position)
        test_context.rhs.assert_called_once_with(tokens, position)
        self.assertIs(result, mock_rhs_result)
