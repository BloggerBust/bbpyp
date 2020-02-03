import unittest
from mock import Mock, PropertyMock, patch, sentinel, DEFAULT, call

from bbpyp.test.mock_helpers import set_property_mock
from bbpyp.lexical_state_machine.lexical_state_machine import LexicalStateMachine
from bbpyp.lexical_state_machine.model.lexical_state import LexicalState


@patch('test.TestContext', create=True)
class TestLexicalStateMachine(unittest.TestCase):

    def setUp(self):
        self._mock_lexical_actions = Mock()
        self._mock_lexical_actions.tokenize = Mock()
        self._mock_lexical_actions.dispatch = Mock()

        self._mock_transition_builder = Mock()
        self._mock_transition_builder.from_state.return_value = self._mock_transition_builder
        self._mock_transition_builder.given_trigger_state.return_value = self._mock_transition_builder
        self._mock_transition_builder.transition_to_state.return_value = self._mock_transition_builder
        self._mock_transition_builder.take_transition_action.return_value = self._mock_transition_builder

        self._mock_transition_builder.provided_guard_is_satisfied.return_value = self._mock_transition_builder
        self._mock_transition_builder.append.return_value = self._mock_transition_builder

        self._mock_transition_builder.build.return_value = {
            (LexicalState.START, LexicalState.PARSE_TAGS): (self._mock_lexical_actions.tokenize, None, LexicalState.PARSE_TAGS),
            (LexicalState.DISPATCH_TOKENS, LexicalState.PARSE_TAGS): (self._mock_lexical_actions.tokenize, None, LexicalState.PARSE_TAGS),
            (LexicalState.PARSE_TAGS, LexicalState.DISPATCH_TOKENS): (self._mock_lexical_actions.dispatch, None, LexicalState.DISPATCH_TOKENS),
        }

    def test_lexical_state_machine_members_initialized_as_expected(self, test_context):

        expected_state = LexicalState.START
        test_context.context_service.get_context_variable.return_value = expected_state
        expected_calls = [call.from_state(LexicalState.START), call.given_trigger_state(LexicalState.PARSE_TAGS), call.take_transition_action(self._mock_lexical_actions.tokenize), call.transition_to_state(LexicalState.PARSE_TAGS), call.append(
        ), call.from_state(LexicalState.DISPATCH_TOKENS), call.append(
        ), call.from_state(LexicalState.PARSE_TAGS), call.given_trigger_state(LexicalState.DISPATCH_TOKENS), call.take_transition_action(self._mock_lexical_actions.dispatch), call.transition_to_state(LexicalState.DISPATCH_TOKENS), call.provided_guard_is_satisfied(LexicalStateMachine._transition_guard_ignore), call.build()]

        state_machine = LexicalStateMachine(
            test_context.logger, self._mock_lexical_actions, self._mock_transition_builder, context_service=test_context.context_service)

        self.assertIs(state_machine._logger, test_context.logger)
        self.assertIs(state_machine._trigger_to_transition,
                      self._mock_transition_builder.build.return_value)
        self.assertIs(state_machine.current_state, expected_state)
        self.assertEqual(self._mock_transition_builder.mock_calls, expected_calls)

    def test_from_starting_state_fire_expected_triggers_and_transition_to_correct_terminal_state(self, test_context):
        def create_case(stimuli_meta_state, starting_state, expected_triggers, expected_terminal_state):
            expected_calls = [call(trigger) for trigger in expected_triggers]

            return {"stimuli_meta_state": stimuli_meta_state, "starting_state": starting_state, "expected_get_trigger_calls": expected_calls, "expected_terminal_state": expected_terminal_state}

        cases = [
            create_case(None, LexicalState.START, [
                (LexicalState.START, LexicalState.PARSE_TAGS),
                (LexicalState.PARSE_TAGS,
                 LexicalState.DISPATCH_TOKENS)
            ], LexicalState.DISPATCH_TOKENS),
            create_case(LexicalState.PARSE_TAGS, LexicalState.PARSE_TAGS, [
                (LexicalState.PARSE_TAGS,
                 LexicalState.DISPATCH_TOKENS)
            ], LexicalState.DISPATCH_TOKENS),
            create_case(LexicalState.DISPATCH_TOKENS, LexicalState.DISPATCH_TOKENS, [
                (LexicalState.DISPATCH_TOKENS,
                 LexicalState.PARSE_TAGS),
                (LexicalState.PARSE_TAGS,
                 LexicalState.DISPATCH_TOKENS)
            ], LexicalState.DISPATCH_TOKENS)
        ]

        with patch('bbpyp.state_machine.abstract_state_machine.AbstractStateMachine.current_state', new_callable=PropertyMock) as current_state_property_spy, patch('bbpyp.message_bus.model.message.Message', autospec=True) as stimuli:

            current_state_property_spy.__set__ = set_property_mock

            for case in cases:
                state_machine = LexicalStateMachine(
                    test_context.logger, self._mock_lexical_actions, self._mock_transition_builder, context_service=test_context.context_service)
                test_context._fire_trigger_spy.reset_mock()
                test_context._fire_trigger_spy.side_effect = state_machine._fire_trigger
                state_machine._fire_trigger = test_context._fire_trigger_spy
                state_machine.current_state = case["starting_state"]
                stimuli.meta = case["stimuli_meta_state"]

                state_machine.next_state(stimuli)

                self.assertIs(state_machine.current_state, case["expected_terminal_state"])
                self.assertEqual(state_machine._fire_trigger.mock_calls,
                                 case["expected_get_trigger_calls"])

    def test_from_starting_state_call_correct_actions(self, test_context):

        def create_case(current_state, action):
            return {"current_state": current_state, "action": action}

        cases = [
            create_case(LexicalState.START, None),
            create_case(LexicalState.PARSE_TAGS, self._mock_lexical_actions.tokenize),
            create_case(LexicalState.DISPATCH_TOKENS, self._mock_lexical_actions.dispatch)
        ]

        with patch('bbpyp.state_machine.abstract_state_machine.AbstractStateMachine.current_state', new_callable=PropertyMock) as current_state_property_spy, patch('bbpyp.message_bus.model.message.Message', autospec=True) as stimuli:
            current_state_property_spy.__set__ = set_property_mock
            stimuli.payload.__set__ = set_property_mock

            for case in cases:
                current_state_property_spy.reset_mock()
                stimuli.reset_mock()
                stimuli.payload.reset_mock()

                self._mock_lexical_actions.tokenize.reset_mock()
                self._mock_lexical_actions.dispatch.reset_mock()

                test_context.next_state.reset_mock()

                state_machine = LexicalStateMachine(
                    test_context.logger, self._mock_lexical_actions, self._mock_transition_builder, context_service=test_context.context_service)
                state_machine.next_state = test_context.next_state
                state_machine.current_state = case["current_state"]

                original_payload = stimuli.payload
                state_machine._on_enter(test_context.previous_state, case["action"], stimuli)

                self.assertEqual(stimuli.meta, case["current_state"])

                if case["current_state"] == LexicalState.START:
                    self._mock_lexical_actions.tokenize.assert_not_called()
                    self._mock_lexical_actions.dispatch.assert_not_called()
                    state_machine.next_state.assert_not_called()
                elif case["current_state"] == LexicalState.PARSE_TAGS:
                    self._mock_lexical_actions.tokenize.called_once_with(original_payload)
                    self.assertEqual(
                        stimuli.payload, self._mock_lexical_actions.tokenize.return_value)
                    self._mock_lexical_actions.dispatch.assert_not_called()
                    state_machine.next_state.assert_called_once_with(stimuli)
                elif case["current_state"] == LexicalState.DISPATCH_TOKENS:
                    self._mock_lexical_actions.tokenize.assert_not_called()
                    self._mock_lexical_actions.dispatch.called_once_with(stimuli)
                    state_machine.next_state.assert_not_called()
