from bbpyp.lexicomb.parser.artifact import Artifact
from bbpyp.lexicomb.parser.model.result import Result


class Variable(Artifact):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = name

    def __repr__(self):
        return f"{self.artifact_name}({self.name})"

    def __call__(self, frame, value):

        value = value.get_value() if isinstance(type(value), Result) else value

        if type(value) is dict and self.name in frame and type(frame[self.name]) is dict:
            frame[self.name] = {**value, **frame[self.name]}
        else:
            frame[self.name] = value

        return frame

    def _eval(self, frame):
        return frame[self.name]

    @property
    def name(self):
        return self._name
