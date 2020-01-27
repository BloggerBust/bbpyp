from enum import Enum
from bbpyp.lexicomb.parser.model.precedence_level_enum import PrecedenceLevelEnum
from bbpyp.lexicomb.parser.model.arity_enum import ArityEnum


class OperatorEnum(Enum):

    LOGICAL_OR = "||"

    LOGICAL_AND = "&&"

    LOGICAL_NEGATION = "!"

    RELATIONAL_LT = "<"
    RELATIONAL_LT_OR_EQ = "<="
    RELATIONAL_EQ = "="
    RELATIONAL_GT = ">"
    RELATIONAL_GT_OR_EQ = ">="
    RELATIONAL_NOT_EQ = "!="

    ARETHMATIC_ADDITION = "+"
    ARETHMATIC_SUBTRACTION = "-"

    ARETHMATIC_MULTIPLICATION = "*"
    ARETHMATIC_DIVISION = "/"

    ARETHMATIC_NEGATIVE = "-"
    ARETHMATIC_POSITIVE = "+"

    def __str__(self):
        return self.value

    def __init__(self, *args):

        self._arity = ArityEnum.TWO

        if not self._is_member_initialized("LOGICAL_OR"):
            self._precedence = PrecedenceLevelEnum.ZERO
        elif not self._is_member_initialized("LOGICAL_AND"):
            self._precedence = PrecedenceLevelEnum.ONE
        elif not self._is_member_initialized("LOGICAL_NEGATION"):
            self._precedence = PrecedenceLevelEnum.TWO
            self._arity = ArityEnum.ONE
        elif not self._is_member_initialized("RELATIONAL_NOT_EQ"):
            self._precedence = PrecedenceLevelEnum.THREE
        elif not self._is_member_initialized("ARETHMATIC_SUBTRACTION"):
            self._precedence = PrecedenceLevelEnum.FOUR
        elif not self._is_member_initialized("ARETHMATIC_DIVISION"):
            self._precedence = PrecedenceLevelEnum.FIVE
        elif not self._is_member_initialized("ARETHMATIC_POSITIVE"):
            self._precedence = PrecedenceLevelEnum.SIX
            self._arity = ArityEnum.ONE

    def __eq__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.precedence == other.precedence

    def __ge__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.precedence >= other.precedence

    def __gt__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.precedence > other.precedence

    def __le__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.precedence <= other.precedence

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            raise NotImplementedError(f"{self} cannot be compared with {other}")
        return self.precedence < other.precedence

    def _is_member_initialized(self, name):
        members = list(self.__class__.__members__)
        return name in members

    @classmethod
    def at_precedence_level(cls, precedence_level):
        return [operator for operator in cls if operator.precedence == operator.precedence & precedence_level][::-1]

    @property
    def precedence(self):
        return self._precedence

    @property
    def arity(self):
        return self._arity
