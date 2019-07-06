from bbp.common.model.transfer_object import TransferObject


class SequentialTransferObject(TransferObject):
    def __init__(self, *args, sequence_service, **kwargs):
        super().__init__(*args, **kwargs)
        self.__sequence_service = sequence_service
        self.__sequence_name = f"{type(self).__module__}.{type(self).__name__}"
        self.__sequence_number = self.__sequence_service.get_next_sequenced_identifier(
            self.sequence_name)

    def __lt__(self, other):
        if self == other:
            return False

        return self.__sequence_service.compare_relative_sequence(self.sequence_name, self.sequence_number, other.sequence_number) == -1

    def __le__(self, other):
        if self == other:
            return True

        return self < other

    def __gt__(self, other):
        if self == other:
            return False

        return self.__sequence_service.compare_relative_sequence(self.sequence_name, self.sequence_number, other.sequence_number) == 1

    def __ge__(self, other):
        if self == other:
            return True

        return self > other

    def free(self):
        self.__sequence_service.remove_sequenced_identifier(
            self.__sequence_name, self.__sequence_number)

        self.__sequence_name = None
        self.__sequence_number = None

    @property
    def sequence_name(self):
        return self.__sequence_name

    @property
    def sequence_number(self):
        return self.__sequence_number
