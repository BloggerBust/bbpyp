import unittest
from mock import patch, create_autospec, sentinel, DEFAULT

from bbpyp.state_machine.state_transition_builder import StateTransitionBuilder


@patch('test.TestContext', create=True)
class TestTransitionBuilder(unittest.TestCase):

    def test_state_transition_builder_from_state_returns_self(self, test_context):
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        self.assertIsInstance(builder.from_state(
            test_context.from_state), StateTransitionBuilder)

    def test_state_transition_builder_from_state_sets_from_state(self, test_context):
        expected = test_context.from_state
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        builder.from_state(test_context.from_state)

        self.assertEqual(builder._from_state, test_context.from_state)

    def test_state_transition_builder_given_trigger_state_returns_self(self, test_context):
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        self.assertIsInstance(builder.given_trigger_state(
            test_context.trigger_state), StateTransitionBuilder)

    def test_state_transition_builder_given_trigger_state_sets_trigger_state(self, test_context):
        expected = test_context.trigger_state
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        builder.given_trigger_state(test_context.trigger_state)

        self.assertEqual(builder._trigger_state, expected)

    def test_state_transition_builder_given_trigger_state_overrides_existing_trigger_state(self, test_context):
        expected = "new trigger state"
        builder = StateTransitionBuilder(test_context.trigger_transition_factory).given_trigger_state(
            test_context.trigger_state)

        builder.given_trigger_state(expected)

        self.assertEqual(builder._trigger_state, expected)

    def test_state_transition_builder_with_trigger_parameter_returns_self(self, test_context):
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        self.assertIsInstance(builder.with_trigger_parameter(
            test_context.trigger_parameter), StateTransitionBuilder)

    def test_state_transition_builder_with_trigger_parameter_sets_trigger_parameter(self, test_context):
        expected = test_context.trigger_parameter
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        builder.with_trigger_parameter(test_context.trigger_parameter)

        self.assertEqual(builder._trigger_parameter, expected)

    def test_state_transition_builder_with_trigger_parameter_overrides_existing_trigger_parameter(self, test_context):
        expected = test_context.trigger_parameter
        builder = StateTransitionBuilder(test_context.trigger_transition_factory).with_trigger_parameter(
            test_context.trigger_parameter)

        builder.with_trigger_parameter(expected)

        self.assertEqual(builder._trigger_parameter, expected)

    def test_state_transition_builder_take_transition_action_returns_self(self, test_context):
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        self.assertIsInstance(builder.take_transition_action(
            test_context.transition_action), StateTransitionBuilder)

    def test_state_transition_builder_take_transition_action_sets_transition_action(self, test_context):
        expected = test_context.transition_action
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        builder.take_transition_action(test_context.transition_action)

        self.assertEqual(builder._transition_action, expected)

    def test_state_transition_builder_take_transition_action_overrides_existing_transition_action(self, test_context):
        expected = test_context.transition_action
        builder = StateTransitionBuilder(test_context.trigger_transition_factory).take_transition_action(
            test_context.transition_action)

        builder.take_transition_action(expected)

        self.assertEqual(builder._transition_action, expected)

    def test_state_transition_builder_provided_guard_is_satisfied_returns_self(self, test_context):
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        self.assertIsInstance(builder.provided_guard_is_satisfied(
            test_context.transition_guard), StateTransitionBuilder)

    def test_state_transition_builder_provided_guard_is_satisfied_sets_transition_guard(self, test_context):
        expected = test_context.transition_guard
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        builder.provided_guard_is_satisfied(test_context.transition_guard)

        self.assertEqual(builder._transition_guard, expected)

    def test_state_transition_builder_without_guard_returns_self(self, test_context):
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        self.assertIsInstance(builder.without_guard(), StateTransitionBuilder)

    def test_state_transition_builder_without_guard_sets_transition_guard_to_None(self, test_context):
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)
        builder._transition_guard = test_context.transition_guard

        builder.without_guard()

        self.assertIsNone(builder._transition_guard)

    def test_state_transition_builder_transition_to_state_overrides_existing_transition_state(self, test_context):
        expected = test_context.transition_state
        builder = StateTransitionBuilder(test_context.trigger_transition_factory).transition_to_state(
            test_context.transition_state)

        builder.transition_to_state(expected)

        self.assertEqual(builder._transition_state, expected)

    def test_state_transition_builder_transition_to_state_returns_self(self, test_context):
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        self.assertIsInstance(builder.transition_to_state(
            test_context.transition_state), StateTransitionBuilder)

    def test_state_transition_builder_transition_to_state_sets_transition_state(self, test_context):
        expected = test_context.transition_state
        builder = StateTransitionBuilder(test_context.trigger_transition_factory)

        builder.transition_to_state(test_context.transition_state)

        self.assertEqual(builder._transition_state, expected)

    def test_state_transition_builder_transition_to_state_overrides_existing_transition_state(self, test_context):
        expected = test_context.transition_state
        builder = StateTransitionBuilder(test_context.trigger_transition_factory).transition_to_state(
            test_context.transition_state)

        builder.transition_to_state(expected)

        self.assertEqual(builder._transition_state, expected)

    @patch('bbpyp.state_machine.model.trigger_transition.TriggerTransition', autospec=True)
    def test_state_transition_builder_append_returns_self(self, trigger_transition_factory, test_context):
        builder = StateTransitionBuilder(trigger_transition_factory)

        self.assertIsInstance(builder.append(), StateTransitionBuilder)

    @patch('bbpyp.state_machine.model.trigger_transition.TriggerTransition', autospec=True)
    def test_state_transition_builder_calling_append_after_setting_new_trigger_increments_transitions_key_length_by_one(self, trigger_transition_factory, test_context):
        expected_initial_transitions_key_length = 0
        builder = StateTransitionBuilder(trigger_transition_factory)

        initial_key_length = len(builder._transitions.keys())

        self.assertEqual(initial_key_length, expected_initial_transitions_key_length)

        expected_transitions_key_length_difference = 1
        builder.given_trigger_state(test_context.trigger_state)

        builder.append()

        self.assertEqual(len(builder._transitions.keys()) - initial_key_length,
                         expected_transitions_key_length_difference)

    @patch('bbpyp.state_machine.model.trigger_transition.TriggerTransition', autospec=True)
    def test_state_transition_builder_calling_append_with_same_trigger_overrides_existing_transition(self, trigger_transition_factory, test_context):

        trigger_transition_factory2 = create_autospec(
            trigger_transition_factory.__class__, spec_set=True)

        trigger_transition1 = trigger_transition_factory(None, None)
        trigger_transition1.trigger = test_context.trigger

        trigger_transition2 = trigger_transition_factory2(None, None)
        trigger_transition2.trigger = test_context.trigger

        self.assertEqual(trigger_transition1.trigger, trigger_transition2.trigger)
        self.assertNotEqual(trigger_transition1.transition, trigger_transition2.transition)

        builder = StateTransitionBuilder(trigger_transition_factory)

        first_transition = builder.append()._transitions[test_context.trigger]
        builder._trigger_transition_factory = trigger_transition_factory2
        second_transition = builder.append()._transitions[test_context.trigger]

        self.assertNotEqual(first_transition, second_transition)

    @patch('bbpyp.state_machine.model.trigger_transition.TriggerTransition', autospec=True)
    def test_state_transition_builder_calling_append_passes_correct_arguments_to_trigger_transition_factory(self, trigger_transition_factory, test_context):
        builder = StateTransitionBuilder(trigger_transition_factory)
        builder._from_state = test_context.from_state
        builder._trigger_state = test_context.trigger_state
        builder._trigger_parameter = test_context.trigger_parameter
        builder._transition_action = test_context.transition_action
        builder._transition_guard = test_context.transition_guard
        builder._transition_state = test_context.transition_state

        expected_trigger = (test_context.from_state, test_context.trigger_state,
                            test_context.trigger_parameter)
        expected_transition = (test_context.transition_action,
                               test_context.transition_guard, test_context.transition_state)

        builder.append()

        trigger_transition_factory.assert_called_once_with(expected_trigger, expected_transition)

    @patch('bbpyp.state_machine.model.trigger_transition.TriggerTransition', autospec=True)
    def test_state_transition_builder_calling_append_with_trigger_parameter_none_does_not_pass_trigger_parameter_to_trigger_transition_factory(self, trigger_transition_factory, test_context):
        builder = StateTransitionBuilder(trigger_transition_factory)
        builder._from_state = test_context.from_state
        builder._trigger_state = test_context.trigger_state
        builder._trigger_parameter = None
        builder._transition_action = test_context.transition_action
        builder._transition_guard = test_context.transition_guard
        builder._transition_state = test_context.transition_state

        expected_trigger = (test_context.from_state, test_context.trigger_state,)
        expected_transition = (test_context.transition_action,
                               test_context.transition_guard, test_context.transition_state)

        builder.append()

        trigger_transition_factory.assert_called_once_with(expected_trigger, expected_transition)

    @patch('bbpyp.state_machine.model.trigger_transition.TriggerTransition', autospec=True)
    def test_state_transition_builder_calling_build_returns_transitions(self, trigger_transition_factory, test_context):
        builder = StateTransitionBuilder(trigger_transition_factory)
        builder.append = test_context.append
        builder.append.return_value = builder

        expected_transitions = {
            (test_context.from_state, test_context.trigger_state,): (test_context.transition_action,
                                                                     test_context.transition_guard, test_context.transition_state),
            (test_context.from_state, test_context.trigger_state, test_context.trigger_parameter1): (test_context.transition_action2,
                                                                                                     test_context.transition_guard2, test_context.transition_state2),
            (test_context.from_state, test_context.trigger_state, test_context.trigger_parameter2): (test_context.transition_action3,
                                                                                                     test_context.transition_guard3, test_context.transition_state3)
        }

        builder._transitions = expected_transitions

        actual_transitions = builder.build()

        builder.append.assert_called_once()

        self.assertEqual(actual_transitions, expected_transitions)
        assert actual_transitions is not expected_transitions
