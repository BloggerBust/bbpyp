import unittest
from mock import PropertyMock, patch, create_autospec

from bbp.ll_combinator.match import Match


@patch('test.TestContext', create=True)
class TestMatch(unittest.TestCase):

    def test_match_initialized_as_expected(self, test_context):
        expected_parser = test_context.parser

        parser = Match(test_context.parser, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                       test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertIs(expected_parser, parser.parser)

    def test_match_string_representation_is_as_expected(self, test_context):
        expected_representation = f"{Match.__name__}({test_context.parser})"

        parser = Match(test_context.parser, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                       test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertEqual(expected_representation, f"{parser}")

    @patch(f"{Match.__module__}.{Match.__name__}.parser", new_callable=PropertyMock)
    @patch('bbp.ll_combinator.model.result.Result', autospec=True)
    def test_match_call_will_call_parser_and_update_parse_progress(self, mock_result, match_parser_property, test_context):

        tokens = [("KEYWMATCHD", "while"), ("SYNTAX", "("), ("SYNTAX", ")")]
        start_position = 0
        mock_result.position = len(tokens)

        test_context.parser.return_value = mock_result
        match_parser_property.return_value = test_context.parser

        parser = Match(test_context.parser, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                       test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory,
                       source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        parser.update_parse_progress = test_context.update_parse_progress_mock

        result = parser(tokens, start_position)

        test_context.parser.assert_called_once_with(tokens, start_position)

        self.assertIs(result, mock_result)
        parser.update_parse_progress.assert_called_once_with(tokens, mock_result.position)
