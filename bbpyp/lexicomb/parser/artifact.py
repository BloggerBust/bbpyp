from abc import ABC, abstractmethod
from bbpyp.common.model.deeply_copyable import DeeplyCopyable


class Artifact(DeeplyCopyable, ABC):
    CALL_STACK_KEY = "$call_stack"
    RESULTS_KEY = "$results"
    IS_UNWINDING_KEY = "$is_unwinding"

    def __init__(self, result_factory, *args, **kwargs):
        self._result_factory = result_factory

    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def _eval(self, frame):
        pass

    @classmethod
    def _has_results_frame(cls, frame):
        return cls.RESULTS_KEY in frame

    @classmethod
    def _get_results_frame(cls, frame):
        if not cls._has_results_frame(frame):
            frame[cls.RESULTS_KEY] = {}
        return frame[cls.RESULTS_KEY]

    @classmethod
    def _set_results_frame(cls, frame, results_frame):
        frame[cls.RESULTS_KEY] = results_frame

    @classmethod
    def _get_call_stack(cls, frame):
        if cls.CALL_STACK_KEY not in frame:
            frame[cls.CALL_STACK_KEY] = []
        return frame[cls.CALL_STACK_KEY]

    @classmethod
    def _set_call_stack(cls, frame, call_stack):
        frame[cls.CALL_STACK_KEY] = call_stack

    @classmethod
    def _get_is_unwinding(cls, frame):
        if cls.IS_UNWINDING_KEY not in frame:
            cls._set_is_unwinding(frame, False)

        return frame[cls.IS_UNWINDING_KEY]

    @classmethod
    def _set_is_unwinding(cls, frame, is_unwinding):
        frame[cls.IS_UNWINDING_KEY] = is_unwinding

    def eval(self, frame):
        return self._eval(frame)

    def eval_and_return_result(self, frame):
        raw_result = self.eval(frame)

        if raw_result is None:
            return self.get_result_aggregate(frame)
        else:
            return self._result_factory(raw_result)

    def get_result_aggregate(self, frame):

        raw_result = self._get_results_frame(frame)
        return self._result_factory(**raw_result)

    @property
    def artifact_name(self):
        return type(self).__name__
