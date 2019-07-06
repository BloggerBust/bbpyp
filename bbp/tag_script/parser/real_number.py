from bbp.tag_script.parser.artifact import Artifact


class RealNumber(Artifact):
    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._number = float(value) if type(value) is str else value
        if type(self._number) is float and self._number.is_integer():
            self._number = int(self._number)

    def __repr__(self):
        return f"{self.artifact_name}({self.value})"

    def _eval(self, frame):
        return self.value

    @property
    def value(self):
        return self._number
