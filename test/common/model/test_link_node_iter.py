import unittest
from mock import patch, create_autospec
from bbpyp.common.model.link_node_iter import LinkNodeIter


@patch("test.TestContext", create=True)
class TestLinkNodeIter(unittest.TestCase):
    def test_members_initialized_as_expected(self, test_context):
        expected_link = test_context.link

        link_iter = LinkNodeIter(test_context.link)

        self.assertIs(link_iter._link, expected_link)

    def test_calling_iter_with_self_returns_self(self, test_context):
        link_iter = LinkNodeIter(test_context.link)
        result = iter(link_iter)

        self.assertIs(result, link_iter)

    def test_calling_next_with_self_returns_link_member(self, test_context):
        expected_link = test_context.link

        link_iter = LinkNodeIter(test_context.link)
        result = next(link_iter)

        self.assertIs(result, expected_link)

    def test_calling_next_with_self_when_link_is_none_raises_stop_iteration_error(self, test_context):
        link_iter = LinkNodeIter(None)
        with self.assertRaises(StopIteration):
            result = next(link_iter)

    def test_calling_next_with_self_multiple_times_iterates_the_link(self, test_context):
        expected_first_link = test_context.link
        expected_second_link = expected_first_link.next_link
        expected_third_link = expected_second_link.next_link

        link_iter = LinkNodeIter(test_context.link)

        self.assertIs(expected_first_link, next(link_iter))
        self.assertIs(expected_second_link, next(link_iter))
        self.assertIs(expected_third_link, next(link_iter))
