import unittest
import re
from mock import patch

from bbp.message_bus.model.message_pipe import MessagePipe
from bbp.message_bus.exception.message_bus_value_error import MessageBusValueError


@patch("test.TestContext", create=True)
class TestMessagePipe(unittest.TestCase):
    def test_members_initialized_as_expected(self, test_context):
        cases = [(test_context.topic,), (test_context.topic, [1, 2, 3],),
                 (test_context.topic, [1, 2, 3], [4, 5, 6])]

        for case in cases:
            pipe = MessagePipe(*case)
            expected_sources = []
            expected_destinations = []

            if len(case) > 2:
                expected_topic, expected_sources, expected_destinations = case
            elif len(case) > 1:
                expected_topic, expected_sources, = case
            else:
                expected_topic, = case

            self.assertIs(pipe.topic, expected_topic)
            self.assertEqual(pipe.sources, expected_sources)
            self.assertEqual(pipe.destinations, expected_destinations)

    def test_initialized_with_invalid_types(self, test_context):

        cases = [(test_context.topic, test_context.bad_source, []),
                 (test_context.topic, [], test_context.bad_destination)]

        for case in cases:
            topic, sources, destinations = case

            if not isinstance(sources, list):
                argument = sources
                argument_name = "sources"
            else:
                argument = destinations
                argument_name = "destinations"

            with self.assertRaisesRegex(MessageBusValueError, re.escape(f"MessageBusValueError: {argument_name}={argument}: {argument_name.title()} must be a list.")):
                MessagePipe(*case)
