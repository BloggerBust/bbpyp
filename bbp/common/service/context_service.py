from contextvars import ContextVar, copy_context
from collections import deque
from bbp.common.exception.bbp_value_error import BbpValueError


class ContextService:

    def __init__(self):
        self._context = ContextVar(f"{self}", default={})
        self._undo_tokens = deque()

    def set_context_variable(self, var_name, var_value):
        context = self._get_context().copy()
        context[var_name] = var_value
        self._set_context(context)

    def get_context_variable(self, var_name):
        context = self._get_context()
        return context[var_name] if var_name in context else None

    def undo(self):
        undo_token = self._pop_undo_token()
        if undo_token is None:
            return

        self._context.reset(undo_token)

    async def run_in_context(self, func, *args, **kwargs):
        if not callable(func):
            raise BbpValueError("func", func, f"must be callable")

        copied_context = copy_context()
        await copied_context.run(func, *args, **kwargs)

    def get_context_key_value_pairs(self):
        copied_context = copy_context()
        values = list(copied_context.values())
        kwargs = values[0] if isinstance(values[0], dict) else values[1]
        return kwargs

    def set_context_key_value_pairs(self, **kwargs):
        for key, value in kwargs.items():
            self.set_context_variable(key, value)

    def _get_context(self):
        return self._context.get({})

    def _set_context(self, context_value):
        undo_token = self._context.set(context_value)
        self._push_undo_token(undo_token)

    def _pop_undo_token(self):
        return self._undo_tokens.pop() if len(self._undo_tokens) > 0 else None

    def _push_undo_token(self, undo_token):
        self._undo_tokens.append(undo_token)
