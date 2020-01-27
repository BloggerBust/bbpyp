from bbpyp.lexicomb.parser.statement import Statement


class ReturnStatement(Statement):

    def __init__(self, expression, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._expression = expression

    def __repr__(self):
        return f"{self.artifact_name}({self._expression})"

    def _eval(self, frame):
        return_value = self._expression.eval(frame)
        self._set_is_unwinding(frame, True)
        return return_value
