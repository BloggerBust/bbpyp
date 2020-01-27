from bbpyp.lexicomb.lexer.error.lexical_error import LexicalError
from bbpyp.lexicomb.lexer.model.tag_enum import TagEnum
from bbpyp.common.model.deeply_copyable import DeeplyCopyable


class Lexer(DeeplyCopyable):
    def __init__(self, logger, tag_expressions_builder):
        self._logger = logger
        self._tag_expressions = tag_expressions_builder.with_tag(
            TagEnum.NONE.value
        ).with_expressions(
            [r"\s+", r"\#.*", r":(?!=)"]
        ).append(
        ).with_tag(
            TagEnum.RESERVED.value
        ).with_expressions(
            [
                r"\@",
                r"\?",
                r"\{",
                r"\}",
                r"\:=",
                r"\(",
                r"\)",
                r"\[",
                r"\]",
                r";",
                r"\+",
                r"-",
                r"\*",
                r"/",
                r"<=",
                r"<",
                r">=",
                r">",
                r"!=",
                r"=",
                r"!",
                r"\|\|",
                r"&&",
                r"return"
            ]
        ).append(
        ).with_tag(
            TagEnum.NUMBER.value
        ).with_expression(
            r"\d+(\.\d*)?"
        ).append(
        ).with_tag(
            TagEnum.TAG.value
        ).with_expression(
            r"[a-zA-Z0-9_]+"
        ).append(
        ).build()

    def tokenize(self, expression):
        tokens = list()
        pos = 0
        while pos < len(expression):
            for tag_expression in self._tag_expressions:
                tag, regular_expressions = tag_expression
                for regex in regular_expressions:
                    match = regex.match(expression, pos)
                    if match:
                        if tag:
                            tokens.append((tag, match.group(0)))
                        break
                else:
                    continue
                pos = match.end(0)
                break
            else:
                error = LexicalError(
                    what=expression, reason=f"error at column {pos} --> {expression[pos]}")
                self._logger.error(error)
                raise error
        return tokens
