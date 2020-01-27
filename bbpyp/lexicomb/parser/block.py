from bbpyp.lexicomb.parser.statement import Statement
from bbpyp.lexicomb.parser.model.result import Result


class Block(Statement):
    def __init__(self, statement_sequence, statement_seperator, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._statement_sequence = statement_sequence
        self._statement_seperator = statement_seperator

    def __repr__(self):
        return f"""{{
        {self._statement_sequence}
        }}"""

    def _eval(self, frame):
        result_value = None
        for statement in self.statement_sequence:
            if statement == self._statement_seperator:
                continue

            next_result_value = statement.eval(frame)
            if self._get_is_unwinding(frame):
                result_value = next_result_value
                break
        return result_value

    @property
    def statement_sequence(self):
        return self._statement_sequence
