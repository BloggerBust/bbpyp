from bbpyp.lexicomb.parser.statement import Statement


class NoOpStatement(Statement):
    def __init__(self, expression, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.artifact_name}()"

    def _eval(self, frame):
        return None
