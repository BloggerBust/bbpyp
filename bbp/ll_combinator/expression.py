from bbp.abstract_parser.parser import Parser
from bbp.tag_script.lexer.model.tag_enum import TagEnum


class Expression(Parser):
    def __init__(self, factor, seperator, match_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._factor = factor
        self._seperator = seperator
        expression_matcher = match_factory(self._factor)
        seperator_matcher = match_factory(self._seperator)
        expression_and_seperator_matcher = expression_matcher | (
            seperator_matcher + expression_matcher)
        self._parser = expression_and_seperator_matcher

    def __repr__(self):
        return f"{type(self).__name__}({self._factor}, {self._seperator})"

    def __call__(self, tokens, position):
        result = self._parser(tokens, position)

        def expand_unary_operator_ast(parsed):
            unary_operator, operand = parsed
            return unary_operator(operand)

        if result.value and isinstance(result.value, tuple):
            result.value = expand_unary_operator_ast(result.value)

        def expand_ast(parsed):
            (seperator, rhs) = parsed
            parser = result.value
            ast = seperator(parser, rhs)
            return ast

        next_node = self._parser >> expand_ast

        try:
            next_result = result
            while next_result.value:
                result = next_result
                next_result = next_node(tokens, result.position)
        except:
            result.value = None

        return result

    @property
    def parser(self):
        return self._parser
