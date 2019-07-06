from bbp.tag_script.parser.artifact import Artifact


class String(Artifact):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._str = value if value is str else str(value)

    def __repr__(self):
        return f"{self.artifact_name}({self._str})"

    def _eval(self, frame):
        return self.value

    @property
    def value(self):
        return self._str
