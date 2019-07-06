from copy import deepcopy
from bbp.common.exception.bbp_value_error import BbpValueError

class DeeplyCopyable:
    _DEEPLY_COPYABLE_ASSIGN_TYPES = set()

    def __deepcopy__(self, memo):
        new_inst = type(self).__new__(self.__class__)
        types_to_assign= self.__types_to_assign()
        def copy_list(source, memo):

            new_list = list()
            for item in source:
                if isinstance(item, (list, tuple)):
                    new_list.append(copy_list(item, memo))
                elif isinstance(item, types_to_assign):
                    new_list.append(item)
                else:
                    new_list.append(deepcopy(item, memo))
            return new_list

        for prop in self.__dict__:
            if isinstance(self.__dict__[prop], types_to_assign):
                new_inst.__dict__[prop] = self.__dict__[prop]
            elif isinstance(self.__dict__[prop], (list, tuple)):
                new_inst.__dict__[prop] = copy_list(self.__dict__[prop], memo)
            else:
                try:
                    new_inst.__dict__[prop] = deepcopy(self.__dict__[prop], memo)
                except:
                    is_deeply_copyable = isinstance(self.__dict__[prop], DeeplyCopyable)
                    if is_deeply_copyable:
                        error_message = "Failed to deeply copy property. A type referenced by type(self.__dict__[prop]) is not deepcopyable. Identify this type and add it to DeeplyCopyable._DEEPLY_COPYABLE_ASSIGN_TYPES"
                    else:
                        error_message = "Failed to deeply copy property. Consider adding type(self.__dict__[prop]) to DeeplyCopyable._DEEPLY_COPYABLE_ASSIGN_TYPES"

                    raise BbpValueError(prop, self.__dict__[prop], error_message)

        return new_inst

    def __copy__(self):
        new_inst = type(self).__new__(self.__class__)
        new_inst.__dict__ = self.__dict__.copy()
        return new_inst

    @classmethod
    def __types_to_assign(cls):
        return tuple(cls._DEEPLY_COPYABLE_ASSIGN_TYPES)
