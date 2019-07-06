from bbp.message_bus.abstract_pub_sub_client import AbstractPubSubClient
from bbp.common.exception.bbp_key_error import BbpKeyError
from bbp.tag_script_engine.model.topic import Topic


class TagScriptPubSubClient(AbstractPubSubClient):
    __STATE_MACHINE_KEY = "STATE_MACHINE_KEY"

    def __init__(self, tag_stream_src, file_stream_service, message_factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._message_factory = message_factory
        self._tag_script_src = tag_stream_src
        self._file_stream_service = file_stream_service
        self._result = None
        self._publish_lines = None
        self._is_file_reader_open = False

    @property
    def result(self):
        return self._result

    async def _process_subscription_message(self, messages):
        messages = messages if isinstance(messages, list) else [messages]

        for message in messages:
            if Topic.REPORT.value == self.topic:
                self._result = message
                await self._async_service.sleep()
            else:
                message_queue_topic = self._context_service.get_context_variable(
                    "message_queue_topic")
                condition = self._get_on_queue_condition(message_queue_topic)
                await self._async_service.on_condition_take_action(condition, self.__state_machine.next_state, message)

    async def _before_subscription(self, state_machine, message_queue_topic, **kwargs):
        self.__state_machine = state_machine
        if message_queue_topic is not None:
            self._context_service.set_context_variable("message_queue_topic", message_queue_topic)
            await self._async_service.sleep()
        else:
            await self._async_service.sleep()

    async def _on_disconnect_subscriber(self, message_queue_topic, **kwargs):
        if self._are_all_queued_topic_events_set(message_queue_topic):
            self._logger.debug(
                "cancelling queue condition for topic message_queue_topic = {}", message_queue_topic)
            condition = self._get_on_queue_condition(message_queue_topic)
            await self._async_service.on_condition_take_action(condition, self._cancel_on_queue_condition, message_queue_topic)

        await super()._on_disconnect_subscriber(message_queue_topic, **kwargs)

    async def _before_publication(self, *args, **kwargs):
        if self._publish_lines is None:
            self._publish_lines = self._file_stream_service.get_io_bound_line_action_worker_thread(
                self._tag_script_src)

    def _create_and_publish_message(self, lines, *args):
        messages = []
        for line in lines:
            messages.append(self._message_factory(line))

        with self._async_service.contextual_action(self.publish_message) as publish_message_context_action:
            self._async_service.from_thread_take_action_in_async(
                publish_message_context_action, messages)

    async def _begin_publication(self):
        self._logger.debug("starting _begin_publication. topic = {}", self.topic)
        if Topic.LEXICAL.value == self.topic:
            with self._async_service.contextual_action(self._create_and_publish_message) as create_and_publish_message_context_action:
                await self._publish_lines(create_and_publish_message_context_action)
        else:
            condition = self._get_on_queue_condition(self.topic)
            while not self._is_queue_empty(self.topic) or not self._are_all_queued_topic_events_set(self.topic):
                if not self._is_queue_poppable(self.topic) and not self._are_all_queued_topic_events_set(self.topic):
                    await self._async_service.on_condition_take_action(condition, condition.wait, octa_is_action_async=True)

                if not self._is_queue_poppable(self.topic):
                    self._logger.debug("the queue is not poppable at this time. Trying again...")
                    continue

                message = self._get_next_queued_message(self.topic)
                await self.publish_message(message)

            assert self._are_all_queued_topic_events_set(self.topic) == True
            assert self._is_queue_empty(self.topic) == True

    async def _after_publication(self):
        # clean up or set end state or whatever....
        await self._async_service.sleep()

    @property
    def __state_machine(self):
        return self._context_service.get_context_variable(type(self).__STATE_MACHINE_KEY)

    @__state_machine.setter
    def __state_machine(self, state_machine):
        self._context_service.set_context_variable(type(self).__STATE_MACHINE_KEY, state_machine)
