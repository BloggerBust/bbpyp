import unittest
from mock import Mock, patch
from os import linesep

from bbpyp.abstract_parser.model.indent_delta import IndentDelta
from bbpyp.common.service.source_format_service import SourceFormatService


@patch('test.TestContext', create=True)
class TestSourceFormatService(unittest.TestCase):

    def setUp(self):
        self._source_format_service = SourceFormatService(format_rules={
            ":=": {"format": [(r"\s*{}\s*", r"{} ")]},
            "+": {"format": [(r"\s*{}\s*", r" {} ")]},
            "-": {"format": [(r"\s*{}\s*", r" {} ")]},
            "*": {"format": [(r"\s*{}\s*", r" {} ")]},
            "/": {"format": [(r"\s*{}\s*", r" {} ")]},
            ";": {"format": [(r"\s*{}\s*", r"{}" + linesep)]},
            "{": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.INCREASE},
            "}": {"format": [(rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{}" + linesep)], "indent_delta": IndentDelta.DECREASE},
            "return": {"format": [(rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{} ")]}
        })

        self._mock_tag = Mock()

        self._tokens = [
            (self._mock_tag, "my_var_0"), (self._mock_tag,
                                           ":="), (self._mock_tag, "0"), (self._mock_tag, ";"),
            (self._mock_tag, "{"),
            (self._mock_tag, "my_var_1"), (self._mock_tag,
                                           ":="), (self._mock_tag, "1"), (self._mock_tag, ";"),
            (self._mock_tag, "{"),
            (self._mock_tag, "my_var_2"), (self._mock_tag,
                                           ":="), (self._mock_tag, "2"), (self._mock_tag, ";"),
            (self._mock_tag, "}"),
            (self._mock_tag, "my_var_3"), (self._mock_tag,
                                           ":="), (self._mock_tag, "3"), (self._mock_tag, ";"),
            (self._mock_tag, "}"),
            (self._mock_tag, "my_var_4"), (self._mock_tag,
                                           ":="), (self._mock_tag, "4"), (self._mock_tag, ";"),

        ]

        self.maxDiff = None

    def test_source_format_service_is_initialized_as_expected(self, test_context):

        actual_format_rules = {
            ":=": {"format": [(r"\s*{}\s*", r"{} ")]},
            "+": {"format": [(r"\s*{}\s*", r" {} ")]},
            "-": {"format": [(r"\s*{}\s*", r" {} ")]},
            "*": {"format": [(r"\s*{}\s*", r" {} ")]},
            "/": {"format": [(r"\s*{}\s*", r" {} ")]},
            ";": {"format": [(r"\s*{}\s*", r"{}" + linesep)]},
            "{": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.INCREASE},
            "}": {"format": [(r"{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.DECREASE},
        }

        expected_format_rules = {
            ":=": {"format": [(r"\s*{}\s*", r"{} ")], "indent_delta": IndentDelta.SAME},
            "+": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
            "-": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
            "*": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
            "/": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
            ";": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.SAME},
            "{": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.INCREASE},
            "}": {"format": [(r"{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.DECREASE},
        }

        expected_increase_indentation_tokens = ['{']
        expected_decrease_indentation_tokens = ['}']
        expected_token_values_with_line_ending_rules = sorted(['{', '}', ';'])

        cases = [(None, 2), (4, 4)]

        for case in cases:
            indentation, expected_indentation = case
            if indentation:
                source_format_service = SourceFormatService(actual_format_rules, indentation)
            else:
                source_format_service = SourceFormatService(actual_format_rules)

            self.assertEqual(expected_format_rules, source_format_service._format_rules)
            self.assertEqual(expected_indentation, source_format_service._indentation)
            self.assertEqual(expected_increase_indentation_tokens,
                             source_format_service._increase_indentation_tokens)
            self.assertEqual(expected_decrease_indentation_tokens,
                             source_format_service._decrease_indentation_tokens)
            self.assertEqual(expected_token_values_with_line_ending_rules,
                             source_format_service._token_values_with_line_ending_rules)

    def test_assignment_is_formatted_as_expected(self, test_context):
        cases = [
            [[(test_context.tag, ":=")], ":= "],
            [[(test_context.tag, "my_var"), (test_context.tag, ":=")], "my_var:= "],
            [[(test_context.tag, "my_var"), (test_context.tag, ":="), (test_context.tag, "0")], "my_var:= 0"],
            [[(test_context.tag, "my_var"), (test_context.tag, ":="),
              (test_context.tag, "0"), (test_context.tag, ";")], f"my_var:= 0;{linesep}"],
            [[(test_context.tag, "my_var"), (test_context.tag, ":="),
              (test_context.tag, "{}"), (test_context.tag, ";")], f"my_var:= {{}};{linesep}"]
        ]

        for case in cases:
            tokens, expected = case
            actual = self._source_format_service.tokens_to_text(tokens)
            self.assertEqual(actual, expected)

    def test_binary_operators_are_formatted_as_expected(self, test_context):
        cases = [
            [[(test_context.tag, "lhs"), (test_context.tag, "+"), (test_context.tag, "rhs")], "lhs + rhs"],
            [[(test_context.tag, "lhs"), (test_context.tag, "-"), (test_context.tag, "rhs")], "lhs - rhs"],
            [[(test_context.tag, "lhs"), (test_context.tag, "*"), (test_context.tag, "rhs")], "lhs * rhs"],
            [[(test_context.tag, "lhs"), (test_context.tag, "/"), (test_context.tag, "rhs")], "lhs / rhs"],
            [[(test_context.tag, "("), (test_context.tag, "lhs1"),  (test_context.tag, "+"), (test_context.tag, "lhs2"),
              (test_context.tag, ")"), (test_context.tag, "/"), (test_context.tag, "rhs")], "(lhs1 + lhs2) / rhs"]
        ]

        for case in cases:
            tokens, expected = case
            actual = self._source_format_service.tokens_to_text(tokens)
            self.assertEqual(actual, expected)

    def test_multiple_statements_are_formatted_as_expected(self, test_context):
        cases = [
            [[(test_context.tag, "my_var_1"), (test_context.tag, ":="), (test_context.tag, "0"), (test_context.tag, ";"),
              (test_context.tag, "my_var_2"), (test_context.tag, ":="), (test_context.tag, "1"), (test_context.tag, ";")], f"my_var_1:= 0;{linesep}my_var_2:= 1;{linesep}"]
        ]

        for case in cases:
            tokens, expected = case
            actual = self._source_format_service.tokens_to_text(tokens)
            self.assertEqual(actual, expected)

    def test_statement_blocks_are_formatted_as_expected(self, test_context):
        indentation_level = 3
        cases = [
            [[
                (test_context.tag, "{"),
                (test_context.tag, "my_var_1"), (test_context.tag,
                                                 ":="), (test_context.tag, "0"), (test_context.tag, ";"),
                (test_context.tag, "my_var_2"), (test_context.tag,
                                                 ":="), (test_context.tag, "1"), (test_context.tag, ";"),
                (test_context.tag, "}")
            ], f"{{{linesep}"
                + f"{'':{indentation_level}}my_var_1:= 0;{linesep}"
                + f"{'':{indentation_level}}my_var_2:= 1;{linesep}"
                + f"}}{linesep}"
            ],
            [[
                (test_context.tag, "my_var_0"), (test_context.tag,
                                                 ":="), (test_context.tag, "0"), (test_context.tag, ";"),
                (test_context.tag, "{"),
                (test_context.tag, "my_var_1"), (test_context.tag,
                                                 ":="), (test_context.tag, "1"), (test_context.tag, ";"),
                (test_context.tag, "{"),
                (test_context.tag, "my_var_2"), (test_context.tag,
                                                 ":="), (test_context.tag, "2"), (test_context.tag, ";"),
                (test_context.tag, linesep), (test_context.tag, linesep),
                (test_context.tag, "}"),
                (test_context.tag, "my_var_3"), (test_context.tag,
                                                 ":="), (test_context.tag, "3"), (test_context.tag, ";"),
                (test_context.tag, "}"),
                (test_context.tag, "my_var_4"), (test_context.tag,
                                                 ":="), (test_context.tag, "4"), (test_context.tag, ";"),

            ], f"my_var_0:= 0;{{{linesep}"
                + f"{'':{indentation_level}}my_var_1:= 1;{{{linesep}"
                + f"{'':{2*indentation_level}}my_var_2:= 2;{linesep}"
                + f"{'':{indentation_level}}}}{linesep}"
                + f"{'':{indentation_level}}my_var_3:= 3;{linesep}"
                + f"}}{linesep}"
                + f"my_var_4:= 4;{linesep}"
            ],

            [[
                (test_context.tag, "?"), (test_context.tag,
                                          "y"), (test_context.tag, "="), (test_context.tag, "x"),
                (test_context.tag, "{"),
                (test_context.tag, "y"), (test_context.tag, ":="), (test_context.tag, "x"), (test_context.tag,
                                                                                             "["), (test_context.tag, "key"), (test_context.tag, "]"), (test_context.tag, ";"),
                (test_context.tag, "}"),
                (test_context.tag, ";"),
                (test_context.tag, "x"), (test_context.tag,
                                          ":="), (test_context.tag, "0"), (test_context.tag, ";")
            ], f"?y=x{{{linesep}"
                + f"{'':{indentation_level}}y:= x[key];{linesep}"
                + f"}};{linesep}"
                + f"x:= 0;{linesep}"]
        ]

        for case in cases:
            tokens, expected = case
            self._source_format_service._indentation = indentation_level
            actual = self._source_format_service.tokens_to_text(tokens)

            self.assertEqual(actual, expected)

    def test_get_indentation_level_of_position(self, test_context):

        cases = [
            ([(test_context.tag, "my_var_0")], 1, 0),
            ([(test_context.tag, "{")], 1, 0),
            ([(test_context.tag, "}")], 1, 0),
            ([(test_context.tag, "{"), (test_context.tag, "my_var_0")], 2, 1),
            (self._tokens, 4, 0),
            (self._tokens, 5, 1),
            (self._tokens, 9, 1),
            (self._tokens, 10, 2),
            (self._tokens, 13, 2),
            (self._tokens, 14, 1),
            (self._tokens, 18, 1),
            (self._tokens, 19, 0),
        ]

        for case in cases:
            tokens, position, expected_indentation_level = case
            indentation_level = self._source_format_service.get_indentation_level_of_position(
                tokens, position)
            self.assertEqual(expected_indentation_level, indentation_level)

    def test_filter_rules_by_indent_delta(self, test_context):
        cases = [
            (IndentDelta.ANY, {":=": {"format": [(r"\s*{}\s*", r"{} ")], "indent_delta": IndentDelta.SAME},
                               "+": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
                               "-": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
                               "*": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
                               "/": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
                               ";": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.SAME},
                               "{": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.INCREASE},
                               "}": {"format": [(rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{}" + linesep)], "indent_delta": IndentDelta.DECREASE},
                               "return": {"format": [(rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{} ")], "indent_delta": IndentDelta.SAME},
                               }),

            (IndentDelta.SAME, {":=": {"format": [(r"\s*{}\s*", r"{} ")], "indent_delta": IndentDelta.SAME},
                                "+": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
                                "-": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
                                "*": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
                                "/": {"format": [(r"\s*{}\s*", r" {} ")], "indent_delta": IndentDelta.SAME},
                                ";": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.SAME},
                                "return": {"format": [(rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{} ")], "indent_delta": IndentDelta.SAME},
                                }),

            (IndentDelta.INCREASE, {
             "{": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.INCREASE}}),
            (IndentDelta.DECREASE, {"}": {"format": [
             (rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{}" + linesep)], "indent_delta": IndentDelta.DECREASE}}),
            (IndentDelta.INCREASE | IndentDelta.DECREASE, {
                "}": {"format": [(rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{}" + linesep)], "indent_delta": IndentDelta.DECREASE},
                "{": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.INCREASE}
            }),
            (~IndentDelta.SAME, {
                "}": {"format": [(rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{}" + linesep)], "indent_delta": IndentDelta.DECREASE},
                "{": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.INCREASE}
            }),

        ]

        case_number = 0
        for case in cases:
            indent_delta_filter, expected_rules = case
            actual_rules = self._source_format_service.filter_rules_by_indent_delta(
                indent_delta_filter)
            self.assertEqual(expected_rules, actual_rules,
                             f"case number {case_number} failed assertion")
            case_number += 1

    def test_get_tokens_between_last_line_separator_and_position(self, test_context):
        cases = [
            ([], -1, []),

            ([(self._mock_tag, ";")], 0, [(self._mock_tag, ";")]),
            ([(self._mock_tag, "{")], 0, [(self._mock_tag, "{")]),
            ([(self._mock_tag, "}")], 0, [(self._mock_tag, "}")]),

            ([(self._mock_tag, ";"), (self._mock_tag, "{")], 1, [
             (self._mock_tag, ";"), (self._mock_tag, "{")]),
            ([(self._mock_tag, ";"), (self._mock_tag, "}")], 1, [(self._mock_tag, "}")]),
            ([(self._mock_tag, ";"), (self._mock_tag, ";")], 1,
             [(self._mock_tag, ";"), (self._mock_tag, ";")]),
            ([(self._mock_tag, "{"), (self._mock_tag, ";")], 1,
             [(self._mock_tag, "{"), (self._mock_tag, ";")]),
            ([(self._mock_tag, "{"), (self._mock_tag, "}")], 1, [(self._mock_tag, "}")]),
            ([(self._mock_tag, "{"), (self._mock_tag, "{")], 1,
             [(self._mock_tag, "{"), (self._mock_tag, "{")]),
            ([(self._mock_tag, "}"), (self._mock_tag, ";")], 1,
             [(self._mock_tag, "}"), (self._mock_tag, ";")]),
            ([(self._mock_tag, "}"), (self._mock_tag, "{")], 1,
             [(self._mock_tag, "}"), (self._mock_tag, "{")]),
            ([(self._mock_tag, "}"), (self._mock_tag, "}")], 1, [(self._mock_tag, "}")]),

            ([(self._mock_tag, "my_var"), (self._mock_tag, ";")], 1,
             [(self._mock_tag, "my_var"), (self._mock_tag, ";")]),
            ([(self._mock_tag, "my_var"), (self._mock_tag, "{")], 1, [
                (self._mock_tag, "my_var"), (self._mock_tag, "{")]),
            ([(self._mock_tag, "my_var"), (self._mock_tag, "}")], 1, [(self._mock_tag, "}")]),

            ([(self._mock_tag, ";"), (self._mock_tag, "my_var")], 1,
             [(self._mock_tag, "my_var")]),
            ([(self._mock_tag, "{"), (self._mock_tag, "my_var")], 1, [
                (self._mock_tag, "my_var")]),
            ([(self._mock_tag, "}"), (self._mock_tag, "my_var")], 1, [(self._mock_tag, "my_var")]),

            ([(self._mock_tag, "my_var_0"), (self._mock_tag, ";"), (self._mock_tag, "{")], 2, [
             (self._mock_tag, "my_var_0"), (self._mock_tag, ";"), (self._mock_tag, "{")]),
            ([(self._mock_tag, "my_var_0"), (self._mock_tag, ";"),
              (self._mock_tag, "}")], 2, [(self._mock_tag, "}")]),
            ([(self._mock_tag, "my_var_0"), (self._mock_tag, ";"), (self._mock_tag, ";")], 2,
             [(self._mock_tag, "my_var_0"), (self._mock_tag, ";"), (self._mock_tag, ";")]),
            ([(self._mock_tag, "my_var_0"), (self._mock_tag, "{"), (self._mock_tag, "{")], 2,
             [(self._mock_tag, "my_var_0"), (self._mock_tag, "{"), (self._mock_tag, "{")]),
            ([(self._mock_tag, "my_var_0"), (self._mock_tag, "{"), (self._mock_tag, "}")], 2,
             [(self._mock_tag, "}")]),
            ([(self._mock_tag, "my_var_0"), (self._mock_tag, "{"), (self._mock_tag, ";")], 2,
             [(self._mock_tag, "my_var_0"), (self._mock_tag, "{"), (self._mock_tag, ";")]),

            ([(self._mock_tag, ";"), (self._mock_tag, "my_var_0"), (self._mock_tag, ":="), (self._mock_tag, "1"), (self._mock_tag, ";")],
             4, [(self._mock_tag, "my_var_0"), (self._mock_tag, ":="), (self._mock_tag, "1"), (self._mock_tag, ";")]),
            ([(self._mock_tag, "}"), (self._mock_tag, "my_var_0"), (self._mock_tag, ":="), (self._mock_tag, "1"), (self._mock_tag, ";")],
             4, [(self._mock_tag, "my_var_0"), (self._mock_tag, ":="), (self._mock_tag, "1"), (self._mock_tag, ";")]),
            ([(self._mock_tag, "{"), (self._mock_tag, "my_var_0"), (self._mock_tag, ":="), (self._mock_tag, "1"), (self._mock_tag, ";")],
             4, [(self._mock_tag, "my_var_0"), (self._mock_tag, ":="), (self._mock_tag, "1"), (self._mock_tag, ";")]),

            (self._tokens, 0, [(self._mock_tag, "my_var_0")]),
            (self._tokens, 3, [(self._mock_tag, "my_var_0"), (self._mock_tag, ":="),
                               (self._mock_tag, "0"), (self._mock_tag, ";")]),
            (self._tokens, 4, [(self._mock_tag, "my_var_0"), (self._mock_tag, ":="),
                               (self._mock_tag, "0"), (self._mock_tag, ";"), (self._mock_tag, "{")]),
            (self._tokens, 5, [(self._mock_tag, "my_var_1")]),
            (self._tokens, 9, [(self._mock_tag, "my_var_1"), (self._mock_tag, ":="), (self._mock_tag, "1"), (self._mock_tag, ";"),
                               (self._mock_tag, "{")]),
            (self._tokens, 10, [(self._mock_tag, "my_var_2")]),
            (self._tokens, 13, [(self._mock_tag, "my_var_2"), (self._mock_tag,
                                                               ":="), (self._mock_tag, "2"), (self._mock_tag, ";")]),
            (self._tokens, 14, [(self._mock_tag, "}")]),
            (self._tokens, 15, [(self._mock_tag, "my_var_3")]),
            (self._tokens, 18, [(self._mock_tag, "my_var_3"), (self._mock_tag,
                                                               ":="), (self._mock_tag, "3"), (self._mock_tag, ";")]),
            (self._tokens, 19, [(self._mock_tag, "}")]),
            (self._tokens, 20, [(self._mock_tag, "my_var_4")]),
            (self._tokens, len(self._tokens) - 1, [(self._mock_tag, "my_var_4"), (self._mock_tag,
                                                                                  ":="), (self._mock_tag, "4"), (self._mock_tag, ";")])
        ]

        for case in cases:
            tokens, position, expected_tokens = case
            actual_tokens = self._source_format_service.get_tokens_between_last_line_separator_and_position(
                tokens, position)
            self.assertEqual(expected_tokens, actual_tokens)

    def test_column_of_position(self, test_context):
        cases = [
            (self._tokens, 0, len("my_var_0")),
            (self._tokens, 3, len("my_var_0:= 0;")),
            (self._tokens, 4, len("my_var_0:= 0;{")),
            (self._tokens, 5, len(f"{'':2}my_var_1")),
            (self._tokens, 8, len(f"{'':2}my_var_1:= 1;")),
            (self._tokens, 9, len(f"{'':2}my_var_1:= 1;{{")),
            (self._tokens, 10, len(f"{'':4}my_var_2")),
            (self._tokens, 13, len(f"{'':4}my_var_2:= 2;")),
            (self._tokens, 14, len(f"{'':2}}}")),
            (self._tokens, 15, len(f"{'':2}my_var_3")),
            (self._tokens, 18, len(f"{'':2}my_var_3:= 4;")),
        ]

        for case in cases:
            tokens, position, expected_column = case
            actual_column = self._source_format_service.get_column_of_position(tokens, position)
            self.assertEqual(expected_column, actual_column)

    def test_get_index_of_next_line_separator_position(self, test_context):
        cases = [
            (self._tokens, 0, 3),
            (self._tokens, 2, 3),
            (self._tokens, 3, 4),
            (self._tokens, 4, 8),
            (self._tokens, 5, 8),
            (self._tokens, 8, 9),
            (self._tokens, 9, 13),
            (self._tokens, 10, 13),
            (self._tokens, 13, 14),
            (self._tokens, 14, 18),
            (self._tokens, 15, 18),
            (self._tokens, 18, 19),
            (self._tokens, 19, 23),
            (self._tokens, 20, 23),
            (self._tokens, 23, 23),
            ([(test_context.tag, "my_var"), (test_context.tag, ":="), (test_context.tag, "{"), (test_context.tag, "}"), (test_context.tag, "my_var"), (test_context.tag, "["), (test_context.tag, "0"), (test_context.tag, "]"), (
                test_context.tag, ":="), (test_context.tag, "{"), (test_context.tag, "}"), (test_context.tag, ";"), (test_context.tag, "return"), (test_context.tag, "my_var"), (test_context.tag, ";")], 4, 9)
        ]

        for case in cases:
            tokens, start_index, expected_index = case
            actual_index = self._source_format_service.get_index_of_next_line_separator_position(
                tokens, start_index)
            self.assertEqual(expected_index, actual_index)
