from bbp.tag_script.parser.artifact import Artifact


class Hash(Artifact):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hash = dict()

    def __repr__(self):
        return f"{self.artifact_name}({self.hash})"

    def _eval(self, frame):
        return self._hash

    @property
    def hash(self):
        return self._hash
