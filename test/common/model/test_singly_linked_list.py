import unittest
from mock import patch, create_autospec
from bbp.common.model.singly_linked_list import SinglyLinkedList


@patch("test.TestContext", create=True)
class TestSinglyLinkedList(unittest.TestCase):

    def spec_factory(self, spec, link_node_iter_factory, instance_accumulator, *args, **kwargs):
        factory = create_autospec(spec, spec_set=True)
        instance = factory(link_node_iter_factory, *args, **kwargs)
        instance_accumulator.append(instance)
        return instance

    def create_spec_factory(self, link_node_iter_factory, accumulator):
        return lambda *args, **kwargs: self.spec_factory(
            self._single_link_node.__class__, link_node_iter_factory, accumulator, *args, **kwargs)

    def setUp(self):
        self._single_link_node_patcher = patch(
            'bbp.common.model.single_link_node.SingleLinkNode', autospec=True)

        self._single_link_node = self._single_link_node_patcher.start()
        self.addCleanup(self._single_link_node_patcher.stop)

    @patch('bbp.common.model.single_link_node.SingleLinkNode', autospec=True)
    def test_members_initialized_as_expected(self, single_link_node, test_context):
        expected_header = single_link_node
        link_factory = test_context.factory
        link_factory.return_value = expected_header

        linked_list = SinglyLinkedList(link_factory)
        self.assertIs(linked_list._linked_node_factory, link_factory)
        self.assertIs(linked_list._header, expected_header)
        self.assertIs(linked_list._tail, None)

    def test_is_empty_returns_expected_result(self, test_context):
        instance_accumulator = []
        link_factory = self.create_spec_factory(test_context.iter_factory, instance_accumulator)

        cases = [(None, True), (test_context.something, False)]

        for case in cases:
            head, expected_is_empty = case
            linked_list = SinglyLinkedList(link_factory)
            linked_list._header.next_link = head
            self.assertEqual(linked_list.is_empty, expected_is_empty)

    def test_calling_insert_the_first_time_sets_the_both_head_and_tail_link(self, test_context):
        instance_accumulator = []
        link_factory = self.create_spec_factory(test_context.iter_factory, instance_accumulator)

        expected_head_value = "foo"

        linked_list = SinglyLinkedList(link_factory)
        header = instance_accumulator[0]
        header.next_link = None

        self.assertIsNone(linked_list.head)

        linked_list.insert(expected_head_value, linked_list.head)
        next_link = instance_accumulator[1]
        next_link.value = expected_head_value

        self.assertEqual(linked_list.head, next_link)
        self.assertEqual(linked_list.head.value, expected_head_value)
        self.assertEqual(linked_list.tail, next_link)

    def test_calling_insert_with_no_link_before_appends_to_tail(self, test_context):

        instance_accumulator = []
        link_factory = self.create_spec_factory(test_context.iter_factory, instance_accumulator)

        expected_head_value = "foo"
        head_link_value = "head link"

        linked_list = SinglyLinkedList(link_factory)
        header = instance_accumulator[0]
        header.next_link = None

        for position in range(1, 10):
            linked_list.insert(test_context.some_value)
            self.assertEqual(linked_list.tail, instance_accumulator[position])

        self.assertEqual(header.next_link, linked_list.head)
        self.assertEqual(linked_list.head, instance_accumulator[1])
        self.assertEqual(linked_list.tail,
                         instance_accumulator[len(instance_accumulator) - 1])

    def test_append_appends_to_tail(self, test_context):

        instance_accumulator = []
        link_factory = self.create_spec_factory(test_context.iter_factory, instance_accumulator)

        expected_head_value = "foo"
        head_link_value = "head link"

        linked_list = SinglyLinkedList(link_factory)
        header = instance_accumulator[0]
        header.next_link = None

        for position in range(1, 10):
            linked_list.append(test_context.some_value)
            self.assertEqual(linked_list.tail, instance_accumulator[position])

        self.assertEqual(header.next_link, linked_list.head)
        self.assertEqual(linked_list.head, instance_accumulator[1])
        self.assertEqual(linked_list.tail,
                         instance_accumulator[len(instance_accumulator) - 1])

    def test_calling_insert_from_inbetween_nodes(self, test_context):

        instance_accumulator = []
        link_factory = self.create_spec_factory(test_context.iter_factory, instance_accumulator)

        expected_insert_value = "foo"

        head_link_value = "head link"
        next_link_value = "next link"

        def get_link_at(header, position):
            count = 0
            link_before = header
            while count < position:
                link_before = link_before.next_link
                count += 1
            return link_before

        for count in range(0, 2):
            instance_accumulator.clear()
            # create a linked list with two nodes
            linked_list = SinglyLinkedList(link_factory)
            header = instance_accumulator[0]
            header.next_link = link_factory(head_link_value)
            original_first_link = instance_accumulator[1]
            original_first_link.value = head_link_value
            header.next_link.next_link = link_factory(next_link_value)
            original_second_link = instance_accumulator[2]
            original_second_link.value = next_link_value

            self.assertIs(linked_list.head, header.next_link)
            self.assertIs(header.next_link, original_first_link)
            self.assertIs(linked_list.head.next_link, header.next_link.next_link)
            self.assertIs(header.next_link.next_link, original_second_link)

            link_before = get_link_at(linked_list.head, count)
            link_after = link_before.next_link

            # insert after head
            linked_list.insert(expected_insert_value, link_before)
            new_link = instance_accumulator[3]
            new_link.value = expected_insert_value
            new_link.next_link = link_after

            self.assertEqual(link_before.next_link, new_link)
            self.assertEqual(link_before.next_link.value, expected_insert_value)
            self.assertEqual(link_before.next_link.next_link, link_after)

    def test_find_returns_link_with_matching_value_or_none_if_no_match(self, test_context):

        instance_accumulator = []
        link_factory = self.create_spec_factory(test_context.iter_factory, instance_accumulator)

        linked_list = SinglyLinkedList(link_factory)
        linked_list._header.next_link = None
        linked_list._tail = None

        linked_list.append(test_context.head_value)
        linked_list.head.value = test_context.head_value
        linked_list.append(test_context.first_value)
        linked_list.head.next_link.value = test_context.first_value
        linked_list.append(test_context.second_value)
        linked_list.head.next_link.next_link.value = test_context.second_value

        linked_list.tail.next_link = None

        cases = [
            (test_context.head_value, linked_list.head),
            (test_context.first_value, linked_list.head.next_link),
            (test_context.second_value, linked_list.head.next_link.next_link),
            (test_context.does_not_exist, None),
        ]

        for case in cases:
            search_value, expected_link = case
            actual_link = linked_list.find(search_value)
            self.assertIs(actual_link, expected_link)
