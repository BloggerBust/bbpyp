import re
from collections import Counter
from os import linesep

from bbp.common.util.collection_util import CollectionUtil
from bbp.common.exception.bbp_value_error import BbpValueError
from bbp.abstract_parser.model.indent_delta import IndentDelta


class SourceFormatService:
    RULE_KEY_FORMAT = "format"
    RULE_KEY_INDENT_DELTA = "indent_delta"

    def __init__(self, format_rules, indentation=2):
        self._indentation = indentation
        self._format_rules = format_rules
        for rule in self._format_rules.values():
            if SourceFormatService.RULE_KEY_INDENT_DELTA not in rule:
                rule[SourceFormatService.RULE_KEY_INDENT_DELTA] = IndentDelta.SAME

        self._increase_indentation_tokens = list(
            self.filter_rules_by_indent_delta(IndentDelta.INCREASE).keys())
        self._decrease_indentation_tokens = list(
            self.filter_rules_by_indent_delta(IndentDelta.DECREASE).keys())

        def contains_filter(collection, index, value): return list(filter(
            lambda item: value in item[index], collection))

        def starts_with_filter(collection, index, value): return list(filter(
            lambda item: item[index].startswith(value), collection))

        def ends_with_filter(collection, index, value): return list(filter(
            lambda item: item[index].endswith(value), collection))

        self._token_values_with_line_ending_rules = SourceFormatService._filter_tokens_by_rules(
            self._format_rules.items(), contains_filter)

        self._token_values_with_leading_line_endings = SourceFormatService._filter_tokens_by_rules(
            self._format_rules.items(), starts_with_filter)

        self._token_values_with_trailing_line_endings = SourceFormatService._filter_tokens_by_rules(
            self._format_rules.items(), ends_with_filter)

    def tokens_to_text(self, tokens):
        text = str()
        indentation_level = 0

        for tag, value in tokens:
            if value in self._format_rules:
                rules = self._format_rules[value]
                indent_delta_rule = rules[SourceFormatService.RULE_KEY_INDENT_DELTA] if SourceFormatService.RULE_KEY_INDENT_DELTA in rules else IndentDelta.SAME

                if indent_delta_rule == IndentDelta.INCREASE:
                    indentation_level += self._indentation
                elif indent_delta_rule == IndentDelta.DECREASE and indentation_level >= self._indentation:
                    indentation_level -= self._indentation

                text = SourceFormatService._append_value_to_text_with_indentation(
                    text, value, indentation_level)

                for format_rule in rules["format"]:
                    search_pattern_template, replace_template = format_rule
                    search_pattern = search_pattern_template.format(re.escape(value)) + "$"
                    replace_string = replace_template.format(value)
                    text = re.sub(search_pattern, replace_string, text)
            else:
                text = SourceFormatService._append_value_to_text_with_indentation(
                    text, value, indentation_level)

        return text

    def get_indentation_level_of_position(self, tokens, position):
        token_values = SourceFormatService._get_token_values(tokens, position)
        last_token_value = token_values[len(token_values) - 1] if len(token_values) else None
        if last_token_value in list(self._increase_indentation_tokens):
            token_values = token_values[:-1]

        token_counter = Counter(token_values)
        indentation_level = sum([token_counter[token]
                                 for token in self._increase_indentation_tokens])
        indentation_level -= sum([token_counter[token]
                                  for token in self._decrease_indentation_tokens])
        if indentation_level < 0:
            indentation_level = 0

        return indentation_level

    def get_tokens_between_last_line_separator_and_position(self, tokens, position):
        token_values = self._get_token_values(tokens, position)
        number_of_tokens = len(tokens)

        reversed_search_from_position = number_of_tokens - 1 if number_of_tokens <= position else position

        if number_of_tokens == 0:
            start_position = 0
        else:

            has_changed = True
            while has_changed and reversed_search_from_position > 0:
                if token_values[reversed_search_from_position] in self._token_values_with_leading_line_endings:
                    start_position = reversed_search_from_position
                    has_changed = False
                else:
                    reversed_search_from_position, has_changed = (
                        reversed_search_from_position - 1, True) if token_values[reversed_search_from_position] in self._token_values_with_line_ending_rules else (reversed_search_from_position, False)

            try:
                start_position = CollectionUtil.reversed_first_index(
                    token_values, self._token_values_with_trailing_line_endings, reversed_search_from_position)
                if start_position < reversed_search_from_position:
                    start_position += 1
            except BbpValueError as e:
                start_position = 0

        return tokens[start_position:position + 1]

    def get_column_of_position(self, tokens, position):
        indentation_level = self.get_indentation_level_of_position(tokens, position)
        line_tokens = self.get_tokens_between_last_line_separator_and_position(tokens, position)
        text = self.tokens_to_text(line_tokens)
        return indentation_level * self._indentation + len(text.strip())

    def get_index_of_next_line_separator_position(self, tokens, start_index):
        next_line_separator_index = start_index
        for index in range(start_index + 1, len(tokens)):
            tag, value = tokens[index]
            next_line_separator_index = index
            if value in self._token_values_with_line_ending_rules:
                break
        return next_line_separator_index

    def filter_rules_by_indent_delta(self, indent_delta_filter):
        return dict(filter(lambda item: indent_delta_filter & item[1][SourceFormatService.RULE_KEY_INDENT_DELTA] != IndentDelta.NONE, self._format_rules.items()))

    @staticmethod
    def _filter_tokens_by_rules(format_rules, format_rule_filter):
        tokens = []
        for token_value, rule in format_rules:
            format_rules = rule[SourceFormatService.RULE_KEY_FORMAT]
            filtered_format_rules = format_rule_filter(format_rules, 1, linesep)
            if len(filtered_format_rules):
                tokens.append(token_value)
        return tokens

    @staticmethod
    def _get_token_values(tokens, position=None):
        if position is not None:
            return [token[1] for token in tokens[:position + 1]]
        else:
            return [token[1] for token in tokens]

    @staticmethod
    def _append_value_to_text_with_indentation(text, value, indentation_level):
        if indentation_level > 0 and len(text) and text[len(text) - 1] == linesep:
            text += f"{'':{indentation_level}}{value}"
        else:
            text += value

        return text
