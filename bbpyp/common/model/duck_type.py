from bbpyp.common.model.equatable_state import EquatableState
from collections import Iterable


class DuckType(EquatableState):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def create_properties(_self, **key_word_args):
            for key, value in key_word_args.items():
                if isinstance(value, str) or not isinstance(value, Iterable):
                    _self.__dict__[key] = value
                elif isinstance(value, dict):
                    _self.__dict__[key] = type(self)(**value)
                else:
                    _self.__dict__[key] = [
                        type(self)(**item) if isinstance(item, dict) else item for item in value]

        if len(args) == 1:
            self.__dict__["$value"] = args[0]
        elif len(args):
            self.__dict__["$value"] = list(args)

        create_properties(self, **kwargs)

    def __repr__(self):
        return f"{type(self).__name__}({self.__dict__})"

    def __str__(self):
        return self.__repr__()

    def get_value(self):
        if self.is_atomic():
            return self.__dict__["$value"]
        else:
            return self.__dict__

    def is_atomic(self):
        return "$value" in self.__dict__.keys() and len(self.__dict__.keys()) == 1
