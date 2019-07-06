import unittest
from mock import patch

from bbp.ll_combinator.defer import Defer


@patch('test.TestContext', create=True)
class TestDefer(unittest.TestCase):

    def test_defer_initialized_as_expected(self, test_context):
        expected_parser_factory = test_context.parser_factory

        parser = Defer(test_context.parser_factory, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                       test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertIs(expected_parser_factory, parser._parser_factory)

    def test_defer_string_representation_is_as_expected(self, test_context):
        expected_representation = f"{Defer.__name__}({test_context.parser_factory})"

        parser = Defer(test_context.parser_factory, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                       test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        self.assertEqual(expected_representation, f"{parser}")

    def test_defer_call_first_time_sets_private_parser_to_parser_factory_result(self, test_context):
        tokens = [("Int", "x"), ("SYNTAX", "+"), ("SYNTAX", "+")]
        position = 0

        parser = Defer(test_context.parser_factory, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                       test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)

        test_context.parser_factory.assert_not_called()

        parser(tokens, position)

        test_context.parser_factory.assert_called_once()

    def test_defer_call_subsequent_times_gets_existing_private_parser_and_does_not_call_parser_factory(self, test_context):
        tokens = [("Int", "x"), ("SYNTAX", "+"), ("SYNTAX", "+")]
        position = 0

        parser = Defer(test_context.parser_factory, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                       test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        parser(tokens, position)
        parser(tokens, position)
        result = parser(tokens, position)

        self.assertEqual(test_context.parser_factory.call_count, 1)
        self.assertIs(parser.parser, test_context.parser_factory.return_value)

    def test_defer_call_results_in_private_parser_being_called_with_expected_parameters(self, test_context):
        mock_parser = test_context.mock_parser_call
        test_context.parser_factory.return_value = mock_parser

        expected_private_parser = mock_parser
        expected_result = mock_parser.return_value

        tokens = [("Int", "x"), ("SYNTAX", "+"), ("SYNTAX", "+")]
        position = 0

        parser = Defer(test_context.parser_factory, test_context.concat_factory, test_context.lhs_or_rhs_factory,
                       test_context.expression_factory, test_context.apply_factory, test_context.greedy_factory, test_context.defer_factory, source_format_service=test_context.source_format_service, context_service=test_context.context_service)
        result = parser(tokens, position)

        self.assertIs(parser.parser, mock_parser)
        mock_parser.assert_called_once_with(tokens, position)
        self.assertIs(result, expected_result)
