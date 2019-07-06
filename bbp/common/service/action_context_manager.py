from contextlib import AbstractContextManager


class ActionContextManager(AbstractContextManager):
    def __init__(self, action, context_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._action = action
        self._context_service = context_service
        self._context_before_enter = None
        
    def __call__(self, *args, **kwargs):
        self._context_service.set_context_key_value_pairs(**self._context_before_enter)
        return self._action(*args, **kwargs)

    def __enter__(self):
        self._context_before_enter = self._context_service.get_context_key_value_pairs()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
