from enum import Enum


class Topic(Enum):
    LEXICAL = "bbp.lexical_state_machine.lexical_analyse"
    PARSE = "bbp.interpreter_state_machine.parse"
    EVALUATE = "bbp.interpreter_state_machine.evaluate"
    REPORT = "bbp.interpreter_state_machine.report"
