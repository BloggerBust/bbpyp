from bbpyp.abstract_parser.parser import Parser as AbstractParser
from bbpyp.lexicomb.lexer.model.tag_enum import TagEnum
from bbpyp.lexicomb.parser.model.operator_enum import OperatorEnum
from bbpyp.lexicomb.parser.model.arity_enum import ArityEnum
from bbpyp.lexicomb.parser.model.precedence_level_enum import PrecedenceLevelEnum
from bbpyp.abstract_parser.exception.parse_error import ParseError


class Parser(AbstractParser):
    def __init__(self,  logger,
                 tag_factory,
                 reserved_factory,
                 repeat_match_factory, variable_factory, real_number_factory,
                 hash_factory, access_factory, unary_operator_factory, binary_operator_factory, select_operator_factory, assignment_factory, block_factory, return_statement_factory, no_op_statement_factory, exist_factory, conditional_factory, conditional_repeat_factory, tag_statement_factory,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logger
        self._tag_factory = tag_factory
        self._reserved_factory = reserved_factory
        self._repeat_match_factory = repeat_match_factory
        self._variable_factory = variable_factory
        self._real_number_factory = real_number_factory
        self._hash_factory = hash_factory
        self._access_factory = access_factory
        self._unary_operator_factory = unary_operator_factory
        self._binary_operator_factory = binary_operator_factory
        self._select_operator_factory = select_operator_factory
        self._assignment_factory = assignment_factory
        self._block_factory = block_factory
        self._return_statement_factory = return_statement_factory
        self._no_op_statement_factory = no_op_statement_factory
        self._exist_factory = exist_factory
        self._conditional_factory = conditional_factory
        self._conditional_repeat_factory = conditional_repeat_factory
        self._tag_statement_factory = tag_statement_factory

        self.build()

    def build(self):

        self._numeric_term = self._tag_factory(TagEnum.NUMBER.value) >> (
            lambda n: self._real_number_factory(n))

        self._numeric_term_negation = (self._create_reserved(
            "!") + self.numeric_term) >> self._unary_operator_factory

        self._hash_term = (self._create_reserved(
            "{") + self._create_reserved("}")) >> (lambda _: self._hash_factory())

        self._tag = self._tag_factory(TagEnum.TAG.value)

        self._name = self.tag >> self._variable_factory

        access_by_factor = (self._create_reserved(
            "[") + (self.name | self.numeric_term | self.hash_term) + self._create_reserved("]")) >> self._ungroup

        self._access_named_container = self._create_named_container(access_by_factor)

        access_by_factor |= (self._create_reserved(
            "[") + self.access_named_container + self._create_reserved("]")) >> self._ungroup

        self._access_named_container |= self._create_named_container(access_by_factor)

        access_by_factor = (self._create_reserved(
            "[") + self.access_named_container + self._create_reserved("]")) >> self._ungroup

        self._existence_check = access_by_factor >> self._exist_factory

        self._arethmatic_expression = self._create_arethmatic_expression_parser()
        self._relational_expression = self._create_relational_expression_parser()
        self._logical_expression = self._create_logical_expression_parser()

        self._tag_expression = self._create_tag_expression()
        self._expression = self.logical_expression | self.relational_expression | self.arethmatic_expression | self._tag_expression

        self._statement_block_begin = self._create_reserved("{")
        self._statement_block_end = self._create_reserved("}")
        self._statement_seperator = self._create_reserved(";")

        self._assignment_statement = self._create_assignment_statement()
        self._conditional_block = self._create_conditional_block()
        self._conditional_repeat_block = self._create_conditional_repeat_block()
        self._return_statement = self._create_return_statement()

        self._tag_statement = self._create_tag_statement()
        self._statement = self._statement_seperator | self.assignment_statement | self._return_statement | self.conditional_repeat_block | self.conditional_block | self._tag_statement | self._tag_expression
        self._statement_sequence = self._create_statement_sequence()
        self._statement_block = self._create_statement_block()

    def __repr__(self):
        # return f"<{type(self).__module__}.{type(self).__name__} object at {hex(id(self))}>()"
        return f"{type(self).__name__}()"

    def __call__(self, tokens, position):
        self.clear_parser_progress()
        self._logger.debug("tokens: {}, position: {}", tokens, position)

        def raise_error(exception=None):
            message = "The parser has encountered an unhandled exception" if exception is not None else "Malformed tagscript encountered. Parsing cannot continue."
            parser_progress = self.get_parser_progress()
            _position = parser_progress["position"] if parser_progress is not None else position

            raise ParseError(tokens, _position, message, inner_exception=exception,
                             source_format_service=self._source_format_service)

        try:
            result = self.statement_block(tokens, position)
        except Exception as e:
            raise_error(e)

        if result.value is None or result.position != len(tokens):
            raise_error()

        self._logger.debug("result: {}", result)
        return result

    def _create_named_container(self, access_by_factor):
        access_by_name_chain = access_by_factor @ self._repeat_match_factory
        return (self.name + access_by_name_chain) >> (lambda arg: self._access_factory(*arg))

    def _create_expression_tree(self, operand_parser, precedence_level):
        factor = operand_parser

        def create_expression(operator_parser):
            return factor * operator_parser

        expression_tree = self._create_operator_expression_parser_with_precedence(
            create_expression, precedence_level)
        parenthesised_expression = (self._create_reserved("(") + expression_tree +
                                    self._create_reserved(")") >> self._ungroup)

        parenthesised_expression_negation = (self._create_reserved(
            "!") + parenthesised_expression) >> (lambda args: self._select_operator_factory(args[0])(args[1]))

        factor |= parenthesised_expression | parenthesised_expression_negation

        return expression_tree

    def _create_arethmatic_expression_parser(self):
        return self._create_expression_tree(self.factor, PrecedenceLevelEnum.FOUR | PrecedenceLevelEnum.FIVE)

    def _create_relational_expression_parser(self):
        factor = self.arethmatic_expression | self.factor
        return self._create_expression_tree(factor, PrecedenceLevelEnum.TWO | PrecedenceLevelEnum.THREE)

    def _create_logical_expression_parser(self):
        factor = self.relational_expression | self.existence_check | self.factor
        logical_expression = self._create_expression_tree(
            factor, PrecedenceLevelEnum.ZERO | PrecedenceLevelEnum.ONE | PrecedenceLevelEnum.TWO)

        return logical_expression

    def _create_operator_expression_parser_with_precedence(self, expression_factory, precedence_level):

        operator_parser = None
        previous_precedence = None
        expression_tree = None
        arity = None
        parser = None

        for operator in OperatorEnum.at_precedence_level(precedence_level):
            if previous_precedence is not None and operator.precedence != previous_precedence:

                if arity == ArityEnum.ONE:
                    parser = operator_parser >> self._select_operator_factory
                    expression_tree = parser @ expression_factory

                elif expression_tree is None:
                    parser = operator_parser >> self._select_operator_factory
                    expression_tree = parser @ expression_factory
                else:
                    parser |= operator_parser >> self._select_operator_factory
                    expression_tree = parser @ expression_factory

                operator_parser = None
                previous_precedence = operator.precedence

            if operator_parser is None:
                operator_parser = self._create_reserved(rf"{operator}")
                previous_precedence = operator.precedence
            else:
                operator_parser |= self._create_reserved(rf"{operator}")

            arity = operator.arity

        parser |= (operator_parser >> self._select_operator_factory)
        if arity == ArityEnum.ONE:
            expression_tree |= (
                operator_parser + expression_tree) >> (lambda args: self._select_operator_factory(args[0])(args[1]))
        else:
            expression_tree *= parser

        return expression_tree

    def _create_tag_expression(self):
        factor_list = self.factor @ self._repeat_match_factory
        stream_line_tag_factor = self.name + factor_list

        return stream_line_tag_factor >> (lambda *args: self._create_tag_statement_ast(*args))

    def _create_tag_statement(self):
        factor_list = self.factor @ self._repeat_match_factory
        tag_factor = self.name + factor_list
        tag_factor_statement = tag_factor + self._statement_seperator
        return tag_factor_statement >> self._create_tag_statement_ast

    def _create_assignment_statement(self):
        source = self.access_named_container | self._name
        destination = self.expression
        return (source + self._create_reserved(":=") + destination + self._statement_seperator) >> self._create_assignment_statement_ast

    def _create_return_statement(self):

        given_expression_return_result = self._create_reserved(
            "return") + self.expression + self._statement_seperator >> self._ungroup

        given_no_expression_do_nothing = self._create_reserved(
            "return") + self._statement_seperator >> self._no_op_statement_factory

        return (given_expression_return_result | given_no_expression_do_nothing) >> self._return_statement_factory

    def _create_statement_block(self):
        block_expression = (self._statement_block_begin + self.statement_sequence +
                            self._statement_block_end) >> self._create_block_ast
        block_expression |= self.statement
        return block_expression

    def _create_conditional_block(self):
        factor = self.logical_expression | self.relational_expression | self.existence_check | self.factor
        conditional_parser = self._create_reserved("?") + factor

        conditional_statement = conditional_parser @ (
            lambda condition: condition + self.statement_block + self.statement_block)
        conditional_statement |= conditional_parser @ (
            lambda condition: condition + self.statement_block + conditional_statement)
        conditional_statement |= conditional_parser @ (
            lambda condition: condition + self.statement_block)

        return conditional_statement >> self._create_conditional_block_ast

    def _create_conditional_repeat_block(self):
        conditional_parser = self._create_reserved("@") + self.conditional_block
        return conditional_parser >> self._create_conditional_repeat_block_ast

    def _create_statement_sequence(self):
        return self.statement @ self._repeat_match_factory

    @property
    def tag(self):
        return self._tag

    @property
    def name(self):
        return self._name

    @property
    def existence_check(self):
        return self._existence_check

    @property
    def access_named_container(self):
        return self._access_named_container

    @property
    def numeric_term(self):
        return self._numeric_term

    @property
    def numeric_term_negation(self):
        return self._numeric_term_negation

    @property
    def hash_term(self):
        return self._hash_term

    @property
    def factor(self):
        return self.access_named_container | self.name | self.numeric_term | self.hash_term

    @property
    def arethmatic_expression(self):
        return self._arethmatic_expression

    @property
    def relational_expression(self):
        return self._relational_expression

    @property
    def logical_expression(self):
        return self._logical_expression

    @property
    def expression(self):
        return self._expression

    @property
    def assignment_statement(self):
        return self._assignment_statement

    @property
    def conditional_block(self):
        return self._conditional_block

    @property
    def conditional_repeat_block(self):
        return self._conditional_repeat_block

    @property
    def statement(self):
        return self._statement

    @property
    def statement_sequence(self):
        return self._statement_sequence

    @property
    def statement_block(self):
        return self._statement_block

    def _get_zero_and_two_of_four(self, expression):
        (((lhs, _), rhs), _) = expression
        return (lhs, rhs)

    def _create_assignment_statement_ast(self, expression):
        arguments = self._get_zero_and_two_of_four(expression)
        return self._assignment_factory(*arguments)

    def _ungroup(self, expression):
        ((_, sub_expression,), _) = expression
        return sub_expression

    def _create_block_ast(self, expression):
        statements = self._ungroup(expression)
        return self._block_factory(statements, self._statement_seperator.value)

    def _create_conditional_block_ast(self, expression):

        def dismember(ast, next_block=None):

            (first, rest), block = ast

            if next_block is None and isinstance(first, tuple):
                return dismember((first, rest), block)

            if isinstance(next_block, tuple):
                next_block = self._create_conditional_block_ast(next_block)

            logical_ast = rest
            if_block_ast = block
            else_block_ast = next_block

            if next_block == self._statement_seperator.value:
                conditional_block_ast = self._conditional_factory(logical_ast, if_block_ast)
            else:
                conditional_block_ast = self._conditional_factory(
                    logical_ast, if_block_ast, else_block_ast)
            return conditional_block_ast

        return dismember(expression)

    def _create_conditional_repeat_block_ast(self, expression):
        _, conditional_ast = expression
        return self._conditional_repeat_factory(conditional_ast)

    def _create_reserved(self, symbol):
        return self._reserved_factory(TagEnum.RESERVED.value, symbol)

    def _create_tag_statement_ast(self, tag_expression):

        tag_statement = None
        if isinstance(tag_expression, tuple):
            tag, rest = tag_expression

            if isinstance(tag, tuple):
                tag, rest = tag

            elif isinstance(rest, tuple):
                next_tag, rest = rest
                rest.insert(0, next_tag)

            if len(rest):
                tag_statement = self._tag_statement_factory(tag, rest)
        return tag_statement
