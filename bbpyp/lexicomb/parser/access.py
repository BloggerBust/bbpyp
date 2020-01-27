from bbpyp.lexicomb.parser.artifact import Artifact


class Access(Artifact):
    def __init__(self, container, keys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._root_container = container
        self._keys = keys

    def __repr__(self):
        return f"{self.artifact_name}:{self._root_container}{self._keys}"

    def __call__(self, frame, value):
        key_value, container = self._get_last_key_and_container(frame)

        if key_value is None:
            container(frame, value)
        else:
            if type(key_value) is int or type(key_value) is float:
                key_value = str(key_value)
            container[key_value] = value
        return frame

    def _eval(self, frame):
        key_value, container = self._get_last_key_and_container(frame)
        if type(container) is not list and type(key_value) is int or type(key_value) is float:
            key_value = str(key_value)
        return container.eval(frame) if key_value is None else container[key_value]

    def _get_last_key_and_container(self, frame):

        container = None
        key_value = None
        if len(self._keys):
            container = self._root_container.eval(frame)
            key_value = self._keys[0].eval(frame)

            for key in self._keys[1:]:
                container = container.eval(frame) if type(
                    container) is Artifact else container[key_value]
                key_value = key.eval(frame)

        container = container if container is not None else self._root_container
        return (key_value, container)

    @property
    def name(self):
        return self._root_container.name
