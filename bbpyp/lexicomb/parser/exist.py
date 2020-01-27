from bbpyp.lexicomb.parser.artifact import Artifact


class Exist(Artifact):
    def __init__(self, term, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._term = term

    def __repr__(self):
        return f"{self.artifact_name}({self._term})"

    def _eval(self, frame):
        does_term_exist_in_scope = False
        try:
            self._term.eval(frame)
            does_term_exist_in_scope = True
        except:
            pass

        return does_term_exist_in_scope
