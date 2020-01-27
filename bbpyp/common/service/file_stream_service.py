from itertools import islice


class FileStreamService:

    def __init__(self, logger, async_service, open_file_service, path_service, context_service, *args, **kwargs):
        self.__logger = logger
        self.__async_service = async_service
        self.__open_file_service = open_file_service
        self.__path_service = path_service
        self.__context_service = context_service

    def is_file(self, file_path):
        return self.__path_service(file_path).is_file()

    def read_text_from_file(self, file_path):
        with self.__open_file_service(file_path) as reader:
            return reader.read()

    def get_lines_reader(self, file_path):
        return lambda: self._line_iterator(open(file_path))

    async def async_action_in_context_of_open_file(self, file_path, action, *args, **kwargs):
        async with self.__async_service.open_file(file_path) as async_file_obj:
            await action(async_file_obj, *args, **kwargs)

    async def async_action_in_context_of_open_file_line_reader(self, file_path, action):
        async def read_next_line_action(reader):
            locked = self.__async_service.lock()
            return await action(lambda: self.async_concurrent_line_iterator(reader, locked))
        await self.async_action_in_context_of_open_file(file_path, read_next_line_action)

    def get_io_bound_line_action_worker_thread(self, file_path, *args, cancellable=False, limiter=None, **open_kwargs):
        rlock = self.__async_service.rlock()
        file_obj = open(file_path, **open_kwargs)
        return lambda line_action, *args: self.__async_service.from_async_take_action_in_thread(self.for_each_batch_take_action, file_obj, rlock, line_action, *args, cancellable=cancellable, limiter=limiter)

    def for_each_line_take_action(self, file_obj, rlock, action, *args, **kwargs):
        for lines in self._lines_iterator(file_obj, rlock):
            for line in lines:
                action(line, *args, **kwargs)

    def for_each_batch_take_action(self, file_obj, rlock, action, *args, **kwargs):
        for lines in self._lines_iterator(file_obj, rlock):
            action(lines, *args, **kwargs)

    async def get_io_bound_line_action_async(self, file_path, line_action, *args, **kwargs):
        locked = self.__async_service.async_lock()
        async_file_obj = await self.__async_service.open_file(file_path)
        return lambda: self.__async_service.from_async_take_action_in_thread(self.for_each_line_take_action, async_file_obj, locked, line_action, *args, **kwargs)

    async def for_each_line_take_action_async(self, file_obj, locked, action, *args, **kwargs):
        async for line in self._line_iterator_async(file_obj, locked):
            await action(*args, **kwargs)

    async def read_text_from_file_async(self, file_path):
        async with await self.__async_service.open_file(file_path) as reader:
            return await reader.read()

    async def read_next_line_from_file_async(self, file_path):
        async with await self.__async_service.open_file(file_path) as lines:
            async for line in lines:
                yield line

    def read_next_line_from_file_start_async(self, file_path):
        return self.__async_service.run(self.read_next_line_from_file_async, file_path)

    async def _line_iterator_async(self, file_obj, locked, chunk_size=1024):
        self.__logger.debug(
            "entered async_concurrent_line_iterator with locked = {}. Is the file object closed? {}", locked, file_obj.closed)
        lines = []
        try:
            while not file_obj.closed:
                async with locked:
                    lines = list(islice(file_obj, chunk_size)) if not file_obj.closed else None

                    for line in lines:
                        if line is None:
                            continue
                        yield line
                    await self.__async_service.sleep()

                if not len(lines):
                    break
        finally:
            if not file_obj.closed:
                file_obj.close()

        self.__logger.debug(
            "leaving async_concurrent_line_iterator file_obj = {}. Is closed = {}", file_obj, file_obj.closed)

    def _line_iterator(self, file_obj):
        with file_obj:
            for line in file_obj:
                if line is None:
                    continue
                yield line

    def _lines_iterator(self, file_obj, rlock, chunk_size=32):
        self.__logger.debug(
            "entered _line_iterator with rlock = {}. Is the file object closed? {}", rlock, file_obj.closed)
        lines = []
        try:
            while not file_obj.closed:
                with rlock:
                    lines = list(islice(file_obj, chunk_size)) if not file_obj.closed else None
                    if not lines:
                        break
                    yield lines

        finally:
            if not file_obj.closed:
                file_obj.close()

        self.__logger.debug("leaving _line_iterator file_obj = {}. Is closed = {}",
                            file_obj, file_obj.closed)
