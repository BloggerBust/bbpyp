import unittest
import re
from mock import patch, DEFAULT

from bbp.state_machine.model.trigger_transition import TriggerTransition
from bbp.state_machine.exception.trigger_value_error import TriggerValueError
from bbp.state_machine.exception.transition_value_error import TransitionValueError


@patch('test.test_context', trigger=("from_something", "given_something"), transition=(
    "take_something", "provided_something", "to_something"), create=True)
class TestTriggerTransition(unittest.TestCase):

    def test_trigger_transition_constructor_with_invalid_trigger_raises_trigger_value_error(
            self, test_context):
        with self.assertRaisesRegex(TriggerValueError, f"TriggerValueError: trigger={test_context.invalid_trigger}: Trigger must be a tuple of length 2 or 3"):
            TriggerTransition(test_context.invalid_trigger, None)

    def test_trigger_transition_constructor_with_trigger_tupple_length_zero_raises_trigger_value_error(
            self, test_context):
        expected_trigger = ()

        with self.assertRaisesRegex(TriggerValueError, re.escape(f"TriggerValueError: trigger={expected_trigger}: Trigger must be a tuple of length 2 or 3")):
            TriggerTransition(expected_trigger, None)

    def test_trigger_transition_constructor_with_trigger_tupple_length_3_raises_trigger_value_error(self, test_context):

        expected_trigger = (1, 2, 3, 4)

        with self.assertRaisesRegex(TriggerValueError, re.escape(f"TriggerValueError: trigger={expected_trigger}: Trigger must be a tuple of length 2 or 3")):
            TriggerTransition(expected_trigger, None)

    def test_trigger_transition_constructor_with_trigger_tupple_length_1_does_not_raise_a_trigger_value_error(
            self, test_context):
        expected_trigger = (1,)

        with self.assertRaisesRegex(TriggerValueError, re.escape(f"TriggerValueError: trigger={expected_trigger}: Trigger must be a tuple of length 2 or 3")):
            TriggerTransition(expected_trigger, None)

    def test_trigger_transition_constructor_with_first_element_none_raises_a_trigger_value_error(self, test_context):
        expected_trigger = (None, None)
        with self.assertRaisesRegex(TriggerValueError, re.escape(f"TriggerValueError: trigger={expected_trigger}: Trigger must not contain empty, 0 or None elements")):
            TriggerTransition(expected_trigger, None)

    def test_trigger_transition_constructor_with_second_element_none_raises_a_trigger_value_error(self, test_context):
        expected_trigger = ("something", None)
        with self.assertRaisesRegex(TriggerValueError, re.escape(f"TriggerValueError: trigger={expected_trigger}: Trigger must not contain empty, 0 or None elements")):
            TriggerTransition(expected_trigger, None)

    def test_trigger_transition_constructor_with_trigger_tupple_length_2_does_not_raise_a_trigger_value_error(self, test_context):
        trigger = ("something", "something")
        TriggerTransition(trigger, test_context.transition)

    def test_trigger_transition_constructor_with_invalid_transition_raises_transition_value_error(
            self, test_context):
        with self.assertRaisesRegex(TransitionValueError, re.escape(f"TransitionValueError: transition={test_context.invalid_transition}: Transition's must be a tupple of length 3")):
            TriggerTransition(test_context.trigger, test_context.invalid_transition)

    def test_trigger_transition_constructor_with_transition_tupple_length_zero_raises_transition_value_error(
            self, test_context):
        expected_transition = ()
        with self.assertRaisesRegex(TransitionValueError, re.escape(f"TransitionValueError: transition={expected_transition}: Transition's must be a tupple of length 3")):
            TriggerTransition(test_context.trigger, expected_transition)

    def test_trigger_transition_constructor_with_transition_tupple_length_1_raises_transition_value_error(
            self, test_context):
        expected_transition = (1)
        with self.assertRaisesRegex(TransitionValueError, re.escape(f"TransitionValueError: transition={expected_transition}: Transition's must be a tupple of length 3")):
            TriggerTransition(test_context.trigger, expected_transition)

    def test_trigger_transition_constructor_with_transition_tupple_length_2_raises_transition_value_error(self, test_context):
        expected_transition = (1, 2)
        with self.assertRaisesRegex(TransitionValueError, re.escape(f"TransitionValueError: transition={expected_transition}: Transition's must be a tupple of length 3")):
            TriggerTransition(test_context.trigger, expected_transition)

    def test_trigger_transition_constructor_with_transition_tupple_length_4_raises_transition_value_error(self, test_context):
        expected_transition = (1, 2, 3, 4)
        with self.assertRaisesRegex(TransitionValueError, re.escape(f"TransitionValueError: transition={expected_transition}: Transition's must be a tupple of length 3")):
            TriggerTransition(test_context.trigger, expected_transition)

    def test_trigger_transition_constructor_with_transition_tupple_length_3_does_not_raise_a_transition_value_error(  # pylint: disable=no-self-use
            self, test_context):
        TriggerTransition(test_context.trigger, test_context.transition)
