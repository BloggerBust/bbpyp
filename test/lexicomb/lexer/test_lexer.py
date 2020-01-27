import unittest
import re
from mock import patch, Mock

from bbpyp.lexicomb.lexer.lexer import Lexer
from bbpyp.lexicomb.lexer.error.tag_expression_value_error import TagExpressionValueError
from bbpyp.lexicomb.lexer.error.lexical_error import LexicalError


@patch('test.TestContext', create=True)
class TestLexer(unittest.TestCase):
    def setUp(self):
        self._mock_tag_expression_builder = Mock()
        self._mock_tag_expression_builder.with_expression.return_value = self._mock_tag_expression_builder
        self._mock_tag_expression_builder.with_expressions.return_value = self._mock_tag_expression_builder
        self._mock_tag_expression_builder.with_tag.return_value = self._mock_tag_expression_builder
        self._mock_tag_expression_builder.append.return_value = self._mock_tag_expression_builder
        self._mock_tag_expression_builder.build.return_value = [
            (None, [re.compile(r"\s+")]),
            ("RESERVED", [re.compile(r":")]),
            ("NUMBER", [re.compile(r"\d+(\.\d*)?")]),
            ("TAG", [re.compile(r"[a-zA-Z0-9_]+")])
        ]

    def test_lexicomb_lexer_lexer_members_initialized_as_expected(self, test_context):
        expected_tag_expressions = [
            (None, [re.compile(r"[ \t\n]+")]),
            ("RESERVED", [re.compile(r":"), re.compile(r"<"), re.compile(r">")])
        ]

        self._mock_tag_expression_builder.build.return_value = expected_tag_expressions

        lexer = Lexer(
            test_context.logger, self._mock_tag_expression_builder)

        self.assertEqual(lexer._tag_expressions, expected_tag_expressions)

    def test_lexicomb_lexer_lexer_calling_tokenize_with_whitespace_characters_should_return_empty_tokens(self, test_context):
        expected_tokens = []
        expression = "    	  	"

        lexer = Lexer(test_context.logger, self._mock_tag_expression_builder)
        tokens = lexer.tokenize(expression)

        self.assertEqual(tokens, expected_tokens)

    def test_lexicomb_lexer_lexer_calling_tokenize_should_return_expected_tokens_tokens(self, test_context):

        self._mock_tag_expression_builder.build.return_value = [
            (None, [re.compile(r"\s+")]),
            ("RESERVED", [re.compile(r":"), re.compile(r"<"), re.compile(r">")]),
            ("NUMBER", [re.compile(r"\d+(\.\d*)?")])
        ]

        lexer = Lexer(test_context.logger, self._mock_tag_expression_builder)
        cases = [
            ([("RESERVED", r":")], ":"),
            ([("RESERVED", r"<"), ("RESERVED", r"<"), ("RESERVED", r"<")], "<<<"),
            ([("RESERVED", r"<"), ("RESERVED", r":"), ("RESERVED", r">")], "<:>"),
            ([("RESERVED", r":"), ("RESERVED", r">"), ("RESERVED", r"<")], " :	 >	<"),
            ([("NUMBER", r"0")], "0"),
            ([("NUMBER", r"4.12")], "4.12"),
            ([("NUMBER", r"1.50"), ("NUMBER", r"01.30")], "1.50 01.30"),
            ([("NUMBER", r"01"), ("RESERVED", r":"), ("NUMBER", r"35"),
              ("NUMBER", r"11"), ("RESERVED", "<"), ("NUMBER", "45")], " 	 01:35  11<45 ")
        ]

        self._assert_cases(cases, lexer)

    def test_lexicomb_lexer_lexer_calling_tokenize_with_valid_expression_should_return_a_list_of_matching_tokens(self, test_context):

        lexer = Lexer(test_context.logger, self._mock_tag_expression_builder)
        cases = [
            ([("TAG", "Driver"), ("TAG", "Trevor")], "Driver Trevor"),
            ([("TAG", "Driver"), ("TAG", "Trevor"), ("TAG", "Wilson")], "Driver Trevor Wilson"),
            ([("TAG", "Trip"),
              ("TAG", "Trevor"), ("TAG", "Wilson"),
              ("NUMBER", "01"), ("RESERVED", ":"), ("NUMBER", "30"),
              ("NUMBER", "10"), ("RESERVED", ":"), ("NUMBER", "45"),
              ("NUMBER", "12.5")],
             "Trip Trevor Wilson 01:30 10:45 12.5")
        ]

        self._assert_cases(cases, lexer)

    def test_lexicomb_lexer_lexer_calling_tokenize_with_invalid_expression_should_raise_an_error(self, test_context):
        lexer = Lexer(test_context.logger, self._mock_tag_expression_builder)

        cases = [
            ([], r"!"),
            ([], r"word @ word"),
            ([], r"word # 1"),
            ([], r"word $ 2"),
            ([], r"word % 2"),
            ([], r"word ^ 2"),
            ([], r"word & 2"),
            ([], r"word * 2"),
            ([], r"word ( 2"),
            ([], r"word ) 2"),
            ([], r"word - 2"),
            ([], r"word + 2"),
            ([], r"word = 2")
        ]

        for expected_tokens, expression in cases:
            with self.assertRaisesRegex(LexicalError, f"LexicalError: {re.escape(expression)}: error at column \d --> \w*"):
                tokens = lexer.tokenize(expression)
                self.assertEqual(tokens, expected_tokens)

    def _assert_cases(self, cases, lexer):
        for expected_tokens, expression in cases:
            tokens = lexer.tokenize(expression)

            self.assertEqual(tokens, expected_tokens)
