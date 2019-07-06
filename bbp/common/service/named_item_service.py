from bbp.common.exception.bbp_key_error import BbpKeyError


class NamedItemService:
    def __init__(self):
        self._named_item = dict()

    def set(self, name, item):
        self._named_item[name] = item

    def set_with_validation(self, name, item, validation_message=None):
        self.validate_does_not_have_name(name, validation_message)
        self._named_item[name] = item

    def get(self, name):
        return self._named_item[name]

    def get_with_validation(self, name, validation_message=None):
        self.validate_has_name(name, validation_message)
        return self.get(name)

    def pop(self, name):
        if self.has(name):
            return self._named_item.pop(name)
        return None

    def has(self, name):
        return name in self._named_item

    def validate_has_name(self, name, validation_message=None):
        if not self.has(name):
            _validation_message = validation_message if validation_message is not None else "named item not found when expected"
            raise BbpKeyError("name", name, _validation_message)

    def validate_does_not_have_name(self, name, validation_message=None):
        if self.has(name):
            _validation_message = validation_message if validation_message is not None else "named item found when not expected"
            raise BbpkKeyError("name", name, _validation_message)

    @property
    def names(self):
        return list(self._named_item.keys())
