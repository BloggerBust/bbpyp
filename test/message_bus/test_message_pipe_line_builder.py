import unittest
import re
from mock import patch, call
from bbpyp.message_bus.message_pipe_line_builder import MessagePipeLineBuilder
from bbpyp.message_bus.exception.message_bus_value_error import MessageBusValueError
from bbpyp.message_bus.abstract_publisher import AbstractPublisher
from bbpyp.message_bus.abstract_subscriber import AbstractSubscriber


@patch("test.TestContext", create=True)
class TestMessagePipeLineBuilder(unittest.TestCase):

    def test_members_initialized_as_expected(self, test_context):
        expected_message_pipe_line_factory = test_context.message_pipe_line_factory

        builder = MessagePipeLineBuilder(test_context.linked_list,
                                         test_context.message_pipe_line_factory)

        self.assertIs(builder._message_pipe_factory, expected_message_pipe_line_factory)
        self.assertIs(builder._topic, None)
        self.assertEqual(len(builder._publishers), 0)
        self.assertEqual(len(builder._subscribers), 0)

    def test_each_method_returns_self_except_build(self, test_context):
        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        builder._validate_pending_components = test_context.turn_off_validation
        builder._validate_topic = test_context.turn_off_validation
        builder._validate_publisher = test_context.turn_off_validation
        builder._validate_subscriber = test_context.turn_off_validation

        result = builder.for_topic(test_context.thingy)
        self.assertIs(result, builder)
        result = builder.with_publisher(test_context.publisher)
        self.assertIs(result, builder)
        result = builder.with_subscriber(test_context.subscriber)
        self.assertIs(result, builder)
        result = builder.append_pipe()
        self.assertIs(result, builder)

    def test_for_topic_sets_topic_member(self, test_context):
        expected_topic = test_context.topic

        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        builder._validate_topic = test_context.turn_off_validation
        builder.for_topic(test_context.topic)

        self.assertIs(builder._topic, expected_topic)

    def test_for_topic_with_invalid_topic_raises_error(self, test_context):
        expected_topic = test_context.topic

        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)

        with self.assertRaisesRegex(MessageBusValueError, re.escape(f"MessageBusValueError: topic={test_context.topic}: The topic provided for the pipeline must be of type [<class 'str'>], but was of type [{type(test_context.topic)}]")):
            builder.for_topic(test_context.topic)

    def test_with_publisher_appends_to_publishers_list(self, test_context):

        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        with patch("bbpyp.message_bus.abstract_publisher.AbstractPublisher", autospec=True) as publisher:
            builder.with_publisher(publisher)
            self.assertEqual(len(builder._publishers), 1)
            self.assertEqual(len(builder._subscribers), 0)
            self.assertIs(builder._publishers[0], publisher)

    def test_with_invalid_publisher_raises_error(self, test_context):
        expected_publisher = test_context.publisher

        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        with self.assertRaisesRegex(MessageBusValueError, re.escape(f"MessageBusValueError: publisher={test_context.publisher}: The publisher being added to the pipeline for topic [None] must be of type [{AbstractPublisher}], but was of type [{type(test_context.publisher)}]")):
            builder.with_publisher(test_context.publisher)

    def test_with_subscriber_appends_to_subscribers_list(self, test_context):
        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        with patch("bbpyp.message_bus.abstract_subscriber.AbstractSubscriber", autospec=True) as subscriber:
            builder.with_subscriber(subscriber)
            actual_subscriber, kwargs = builder._subscribers[0]
            self.assertEqual(len(builder._subscribers), 1)
            self.assertEqual(len(builder._publishers), 0)
            self.assertIs(actual_subscriber, subscriber)
            self.assertEqual(kwargs, {})

            builder.with_subscriber(subscriber, arg1=test_context.arg1, arg2=test_context.arg2)
            actual_subscriber, kwargs = builder._subscribers[1]
            self.assertEqual(len(builder._subscribers), 2)
            self.assertIs(actual_subscriber, subscriber)
            self.assertEqual(kwargs, {"arg1": test_context.arg1, "arg2": test_context.arg2})

    def test_with_invalid_subscriber_raises_error(self, test_context):
        expected_subscriber = test_context.subscriber

        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        with self.assertRaisesRegex(MessageBusValueError, re.escape(f"MessageBusValueError: subscriber={test_context.subscriber}: The subscriber being added to the pipeline for topic [None] must be of type [{AbstractSubscriber}], but was of type [{type(test_context.subscriber)}]")):
            builder.with_subscriber(test_context.subscriber)

    def test_append_pipe_clears_topic_publishers_and_subscribers(self, test_context):
        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        builder._validate_pending_components = test_context.turn_off_validation
        builder._topic = test_context.topic
        builder._publishers = [1, 2, 3]
        builder._subscribers = [4, 5, 6]

        builder.append_pipe()

        self.assertIsNone(builder._topic)
        self.assertEqual(len(builder._publishers), 0)
        self.assertEqual(len(builder._subscribers), 0)

    def test_append_pipe_calls_message_pipe_factory_with_correct_arguments(self, test_context):

        expected_topic = test_context.topic
        expected_publishers = [1, 2, 3]
        expected_subscribers = [4, 5, 6]

        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        builder._message_pipe_factory = test_context.message_pipe_factory
        builder._validate_pending_components = test_context.turn_off_validation
        builder._topic = expected_topic
        builder._publishers = expected_publishers.copy()
        builder._subscribers = expected_subscribers.copy()

        builder.append_pipe()

        test_context.message_pipe_factory.assert_called_once_with(
            test_context.topic, expected_publishers, expected_subscribers)

        (arg_topic, arg_publishers, arg_subscribers), _ = test_context.message_pipe_factory.call_args

        self.assertEqual(arg_topic, expected_topic)
        self.assertEqual(arg_publishers, expected_publishers)
        self.assertEqual(arg_subscribers, expected_subscribers)

        self.assertIs(arg_topic, expected_topic)
        self.assertIsNot(arg_publishers, expected_publishers)
        self.assertIsNot(arg_subscribers, expected_subscribers)

    def test_append_pipe_does_nothing_if_no_fields_are_set(self, test_context):
        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        builder._message_pipe_factory = test_context.message_pipe_factory

        result = builder.append_pipe()

        builder._message_pipe_factory.assert_not_called()
        self.assertEqual(result, builder)
        self.assertFalse(len(builder._pipe_line))

    @patch("bbpyp.message_bus.abstract_subscriber.AbstractSubscriber", autospec=True)
    @patch("bbpyp.message_bus.abstract_publisher.AbstractPublisher", autospec=True)
    def test_append_pipe_raises_error_if_missing_or_invalid_fields(self, publisher, subscriber, test_context):

        cases = [
            (None, [publisher], [subscriber], re.escape(
                "MessageBusValueError: topic=None: The topic provided for the pipeline must be of type [<class 'str'>], but was of type [<class 'NoneType'>]")),

            ("topic.foo", [], [subscriber], re.escape(
                f"MessageBusValueError: publishers=[]: The publisher collection being added to the pipeline for topic [topic.foo] must be none empty")),
            ("topic.foo", [test_context.bad_publisher], [subscriber], re.escape(
                f"MessageBusValueError: publisher={test_context.bad_publisher}: The publisher being added to the pipeline for topic [topic.foo] must be of type [{AbstractPublisher}], but was of type [{type(test_context.bad_publisher)}]")),

            ("topic.foo", [publisher], [], re.escape(
                f"MessageBusValueError: subscribers=[]: The subscriber collection being added to the pipeline for topic [topic.foo] must be none empty")),
            ("topic.foo", [publisher], [(test_context.bad_subscriber, {})], re.escape(
                f"MessageBusValueError: subscriber={test_context.bad_subscriber}: The subscriber being added to the pipeline for topic [topic.foo] must be of type [{AbstractSubscriber}], but was of type [{type(test_context.bad_subscriber)}]"))
        ]

        for case in cases:
            builder = MessagePipeLineBuilder(
                test_context.linked_list, test_context.pipe_line_factory)

            builder._topic, builder._publishers, builder._subscribers, error = case

            with self.assertRaisesRegex(MessageBusValueError, error):
                builder.append_pipe()

    def test_build_returns_pipe_line(self, test_context):
        builder = MessagePipeLineBuilder(test_context.linked_list, test_context.pipe_line_factory)
        builder._pipe_line = test_context.pipe_line

        result = builder.build()

        self.assertEqual(result, test_context.pipe_line)

    def test_build_calls_append_pipe(self, test_context):

        builder = MessagePipeLineBuilder(
            test_context.linked_list, test_context.pipe_line_factory)
        builder.append_pipe = test_context.append_pipe

        builder.build()

        test_context.append_pipe.assert_called_once()
