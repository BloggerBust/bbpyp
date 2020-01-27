import threading
import trio
from math import inf as infinity
from async_generator import aclosing
from io import IOBase


class AsyncService:
    def __init__(self, logger, context_service, action_context_factory, memory_channel_max_buffer_size):
        self._logger = logger
        self._context_service = context_service
        self._action_context_factory = action_context_factory
        self._memory_channel_max_buffer_size = memory_channel_max_buffer_size

    @classmethod
    def run(cls, *args, **kwargs):
        trio.run(*args, **kwargs)

    @classmethod
    async def sleep(cls, seconds=0):
        await trio.sleep(seconds)

    @classmethod
    async def open_file(cls, *args, **kwargs):
        file_path = args[0]
        rest = args[1:]

        if isinstance(file_path, IOBase):
            return trio.wrap_file(file_path)

        return await trio.open_file(file_path, *rest, **kwargs)

    @classmethod
    def close_file(cls, async_open_file):
        return aclosing(async_open_file)

    @classmethod
    def async_lock(cls):
        return trio.Lock()

    @classmethod
    def rlock(cls, do_block=True):
        return threading.RLock(do_block)

    def contextual_action(self, action):
        return self._action_context_factory(action)

    async def from_async_take_action_in_thread(self, action, *args, cancellable=False, limiter=None):
        await trio.to_thread.run_sync(action, *args, cancellable=cancellable, limiter=limiter)

    def from_thread_take_action_in_async(self, async_action, *args, trio_token=None):
        trio.from_thread.run(async_action, *args, trio_token=trio_token)

    @classmethod
    def condition(cls, lock=None):
        return trio.Condition(lock)

    async def on_condition_take_action(self, condition, action, *args, octa_timeout=infinity, octa_is_action_async=False, **kwargs):
        self._logger.debug(
            "wait up to {} seconds for condition {} then take action = {} with args = {} else cancell action", octa_timeout, condition, action, args)
        result = None
        start_time = self.get_time()
        with trio.move_on_after(octa_timeout) as cancel_scope:
            async with condition:
                elapsed_time = self.get_time() - start_time
                self._logger.debug("on_condition after {}s", elapsed_time)
                if octa_is_action_async:
                    result = await action(*args, **kwargs)
                else:
                    result = action(*args, **kwargs)
            elapsed_time = self.get_time() - start_time
            if cancel_scope.cancelled_caught:
                self._logger.warn("action cancelled after {}s", elapsed_time)
            else:
                self._logger.debug("action completed after {}s", elapsed_time)

        return result

    def multi_error_handler_context(self, handler=None, do_print_stack_trace=False):

        def handle_exception(exec):
            self._logger.error(exec, exc_info=do_print_stack_trace)
            return exec

        return trio.MultiError.catch(handle_exception if handler is None else handler)

    @classmethod
    def create_cancellable_scope(cls, **kwargs):
        return trio.CancelScope(**kwargs)

    @classmethod
    def create_channel_context(cls):
        return trio.open_nursery()

    def create_channel(self):
        return trio.open_memory_channel(self._memory_channel_max_buffer_size)

    @classmethod
    def create_event(cls):
        return trio.Event()

    @classmethod
    def get_time(cls):
        return trio.current_time()
