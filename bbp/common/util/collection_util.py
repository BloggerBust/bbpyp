from bbp.common.model.deeply_copyable import DeeplyCopyable
from bbp.common.exception.bbp_value_error import BbpValueError


class CollectionUtil:
    @staticmethod
    def add_items(collection, *items):
        if hasattr(collection, 'update'):
            collection.update(items)
        elif hasattr(collection, 'append'):
            for item in items:
                collection.append(item)
        elif hasattr(collection, 'add'):
            for item in items:
                collection.add(item)

    @staticmethod
    def add_types_to_deepcopy_direct_assignment_list(*types_to_be_directly_assigned):
        CollectionUtil.add_items(DeeplyCopyable._DEEPLY_COPYABLE_ASSIGN_TYPES,
                                 *types_to_be_directly_assigned)

    @staticmethod
    def reversed_index(collection, item, from_position=None):
        from_position = from_position if from_position is not None else len(collection) - 1
        for index in reversed(range(0, from_position + 1)):
            if collection[index] == item:
                return index
        raise BbpValueError("item", item, "is not in collection" if from_position == len(
            collection) - 1 else f"is not in collection before position {from_position}")

    @staticmethod
    def reversed_first_index(collection, items, from_position=None):
        from_position = from_position if from_position is not None else len(collection) - 1

        for index in reversed(range(0, from_position + 1)):
            if collection[index] in items:
                return index
        raise BbpValueError("items", items, "are not in collection" if from_position == len(
            collection) - 1 else f"are not in collection before position {from_position}")
