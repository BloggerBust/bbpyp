from bbpyp.lexicomb.parser.statement import Statement
from bbpyp.lexicomb.parser.model.result import Result


class ConditionalRepeat(Statement):
    def __init__(self, conditional_block, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conditional_block = conditional_block

    def __repr__(self):
        return f"@{self._conditional_block}"

    def _eval(self, frame):
        result_value = None
        while self.is_any_condition_satisfied(frame):
            next_value = self._conditional_block.eval(frame)
            if self._get_is_unwinding(frame):
                result_value = next_value
                break

        return result_value

    def is_any_condition_satisfied(self, frame):
        return self._conditional_block.is_any_condition_satisfied(frame)
