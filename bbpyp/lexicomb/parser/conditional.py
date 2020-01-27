from bbpyp.lexicomb.parser.statement import Statement


class Conditional(Statement):
    def __init__(self, condition, if_block, else_block=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._condition = condition
        self._if_block = if_block
        self._else_block = else_block

    def __repr__(self):
        return f"(? {self._condition} {self._if_block} {self._else_block})"

    def _eval(self, frame):
        if self.is_condition_satisfied(frame):
            return self._if_block.eval(frame)
        elif self._else_block is not None:
            return self._else_block.eval(frame)

        return frame

    def is_condition_satisfied(self, frame):
        return self._condition.eval(frame)

    def is_any_condition_satisfied(self, frame):
        return self.is_condition_satisfied(frame) if self.is_condition_satisfied(frame) or not isinstance(self._else_block, Conditional) else self._else_block.is_condition_satisfied(frame)
