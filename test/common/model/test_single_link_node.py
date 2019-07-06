import unittest
import re
from mock import patch, create_autospec
from bbp.common.model.single_link_node import SingleLinkNode
from bbp.common.exception.bbp_value_error import BbpValueError


@patch("test.TestContext", create=True)
class TestSingleLinkNode(unittest.TestCase):

    def test_members_initialized_as_expected(self, test_context):

        cases = [
            (None, None),
            (test_context.expected_value, None),
            (test_context.expected_value, SingleLinkNode(
                test_context.link_node_iter_factory)),
            (test_context.expected_value, test_context.bad_value)
        ]

        for case in cases:
            expected_value, expected_next_link = case

            if expected_next_link is test_context.bad_value:
                with self.assertRaisesRegex(BbpValueError, re.escape(rf"{expected_next_link}: Must be either None or of type {SingleLinkNode}")):
                    SingleLinkNode(expected_value, expected_next_link,
                                   link_node_iter_factory=test_context.link_node_iter_factory)
                continue

            link = SingleLinkNode(expected_value, expected_next_link,
                                  link_node_iter_factory=test_context.link_node_iter_factory)
            self.assertIs(link._value, expected_value)
            self.assertIs(link._next_link, expected_next_link)
            self.assertIs(link.value, expected_value)
            self.assertIs(link.next_link, expected_next_link)

    def test_getting_and_setting_link_value(self, test_context):
        expected_value = test_context.value
        link = SingleLinkNode(link_node_iter_factory=test_context.link_node_iter_factory)
        self.assertIs(link.value, None)

        link.value = test_context.value

        self.assertIs(link.value, expected_value)

    def test_getting_and_setting_next_link(self, test_context):
        expected_next_link = SingleLinkNode(
            test_context.link_node_iter_factory)
        link = SingleLinkNode(link_node_iter_factory=test_context.link_node_iter_factory)
        self.assertIs(link.next_link, None)

        link.next_link = expected_next_link

        self.assertIs(link.next_link, expected_next_link)

    def test_calling_iter_with_self_returns_result_from_iter_factory(self, test_context):
        expected_iterator = test_context.link_node_iter_factory.return_value

        link = SingleLinkNode(link_node_iter_factory=test_context.link_node_iter_factory)
        link_iter = iter(link)

        self.assertIs(link_iter, expected_iterator)
