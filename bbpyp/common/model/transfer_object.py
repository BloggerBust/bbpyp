from bbpyp.common.model.equatable_state import EquatableState


class TransferObject(EquatableState):
    def __init__(self, payload, meta=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__payload = payload
        self.__meta = meta

    @property
    def payload(self):
        return self.__payload

    @payload.setter
    def payload(self, value):
        self.__payload = value

    @property
    def meta(self):
        return self.__meta

    @meta.setter
    def meta(self, value):
        self.__meta = value
