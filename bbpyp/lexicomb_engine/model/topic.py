from enum import Enum


class Topic(Enum):
    LEXICAL = "bbpyp.lexical_state_machine.lexical_analyse"
    PARSE = "bbpyp.interpreter_state_machine.parse"
    EVALUATE = "bbpyp.interpreter_state_machine.evaluate"
    REPORT = "bbpyp.interpreter_state_machine.report"
