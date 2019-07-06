import unittest
from mock import Mock, PropertyMock, patch, call

from test.mock_helpers import set_property_mock
from bbp.interpreter_state_machine.interpreter_state import InterpreterState
from bbp.interpreter_state_machine.interpreter_state_machine import InterpreterStateMachine


@patch('test.TestContext', create=True)
class TestInterpreterStateMachine(unittest.TestCase):
    def setUp(self):
        self._mock_actions = Mock()
        self._mock_actions.parse = Mock()
        self._mock_actions.dispatch = Mock()
        self._mock_actions.evaluate = Mock()
        self._mock_actions.report = Mock()

        self._mock_transition_builder = Mock()
        self._mock_transition_builder.from_state.return_value = self._mock_transition_builder
        self._mock_transition_builder.given_trigger_state.return_value = self._mock_transition_builder
        self._mock_transition_builder.transition_to_state.return_value = self._mock_transition_builder
        self._mock_transition_builder.take_transition_action.return_value = self._mock_transition_builder
        self._mock_transition_builder.append.return_value = self._mock_transition_builder

        self._mock_transition_builder.build.return_value = {
            (InterpreterState.START, InterpreterState.PARSE_TOKENS): (self._mock_actions.parse, None, InterpreterState.PARSE_TOKENS),
            (InterpreterState.DISPATCH_PARSER, InterpreterState.PARSE_TOKENS): (self._mock_actions.parse, None, InterpreterState.PARSE_TOKENS),
            (InterpreterState.PARSE_TOKENS, InterpreterState.DISPATCH_PARSER): (self._mock_actions.dispatch, None, InterpreterState.DISPATCH_PARSER),
            (InterpreterState.START, InterpreterState.EVALUATE): (self._mock_actions.evaluate, None, InterpreterState.EVALUATE),
            (InterpreterState.REPORT_RESULT, InterpreterState.EVALUATE): (self._mock_actions.evaluate, None, InterpreterState.EVALUATE),
            (InterpreterState.EVALUATE, InterpreterState.REPORT_RESULT): (self._mock_actions.report, None, InterpreterState.REPORT_RESULT)
        }

    def test_interpreter_state_machine_members_initialized_as_expected(self, test_context):

        expected_state = InterpreterState.START
        expected_actions = self._mock_actions
        expected_frame = {}
        expected_calls = [
            call.from_state(InterpreterState.START), call.given_trigger_state(InterpreterState.PARSE_TOKENS), call.take_transition_action(self._mock_actions.parse), call.transition_to_state(InterpreterState.PARSE_TOKENS), call.append(
            ), call.from_state(InterpreterState.DISPATCH_PARSER), call.append(
            ), call.from_state(InterpreterState.PARSE_TOKENS), call.given_trigger_state(InterpreterState.DISPATCH_PARSER), call.take_transition_action(self._mock_actions.dispatch), call.transition_to_state(InterpreterState.DISPATCH_PARSER), call.append(
            ), call.from_state(InterpreterState.START), call.given_trigger_state(InterpreterState.EVALUATE), call.take_transition_action(self._mock_actions.evaluate), call.transition_to_state(InterpreterState.EVALUATE), call.append(
            ), call.from_state(InterpreterState.REPORT_RESULT), call.append(
            ), call.from_state(InterpreterState.EVALUATE), call.given_trigger_state(InterpreterState.REPORT_RESULT), call.take_transition_action(self._mock_actions.report), call.transition_to_state(InterpreterState.REPORT_RESULT),
            call.build()
        ]

        test_context.context_service.get_context_variable.return_value = expected_state
        state_machine = InterpreterStateMachine(
            test_context.logger, self._mock_actions, self._mock_transition_builder, context_service=test_context.context_service)

        self.assertIs(state_machine._logger, test_context.logger)
        self.assertIs(state_machine._actions, expected_actions)
        self.assertEqual(state_machine._frame, expected_frame)

        self.assertIs(state_machine._trigger_to_transition,
                      self._mock_transition_builder.build.return_value)
        self.assertIs(state_machine.current_state, expected_state)

        self.assertEqual(self._mock_transition_builder.mock_calls, expected_calls)

    def test_from_starting_state_fire_expected_triggers_and_transition_to_correct_terminal_state(self, test_context):

        def create_case(stimuli_meta_state, starting_state, expected_triggers, expected_terminal_state):
            expected_calls = [call(trigger) for trigger in expected_triggers]
            return {"stimuli_meta_state": stimuli_meta_state, "starting_state": starting_state, "expected_get_trigger_calls": expected_calls, "expected_terminal_state": expected_terminal_state}

        cases = [
            create_case(None, InterpreterState.START, [
                (InterpreterState.START, InterpreterState.PARSE_TOKENS),
                (InterpreterState.PARSE_TOKENS, InterpreterState.DISPATCH_PARSER),
            ], InterpreterState.DISPATCH_PARSER),

            create_case(InterpreterState.PARSE_TOKENS, InterpreterState.PARSE_TOKENS, [
                (InterpreterState.PARSE_TOKENS, InterpreterState.DISPATCH_PARSER),
            ], InterpreterState.DISPATCH_PARSER),

            create_case(InterpreterState.DISPATCH_PARSER, InterpreterState.START, [
                (InterpreterState.START, InterpreterState.EVALUATE),
                (InterpreterState.EVALUATE, InterpreterState.REPORT_RESULT),
            ], InterpreterState.REPORT_RESULT),

            create_case(InterpreterState.EVALUATE, InterpreterState.EVALUATE, [
                (InterpreterState.EVALUATE, InterpreterState.REPORT_RESULT),
            ], InterpreterState.REPORT_RESULT),

            create_case(InterpreterState.DISPATCH_PARSER, InterpreterState.REPORT_RESULT, [
                (InterpreterState.REPORT_RESULT, InterpreterState.EVALUATE),
                (InterpreterState.EVALUATE, InterpreterState.REPORT_RESULT),
            ], InterpreterState.REPORT_RESULT),

        ]

        with patch('bbp.state_machine.abstract_state_machine.AbstractStateMachine.current_state', new_callable=PropertyMock) as current_state_property_spy, patch('bbp.message_bus.model.message.Message', autospec=True) as stimuli:
            current_state_property_spy.__set__ = set_property_mock

            for case in cases:
                current_state_property_spy.reset_mock()
                test_context._fire_trigger_spy.reset_mock()
                stimuli.reset_mock()

                current_state_property_spy.return_value = case["starting_state"]

                state_machine = InterpreterStateMachine(
                    test_context.logger, self._mock_actions, self._mock_transition_builder, context_service=test_context.context_service)

                stimuli.meta = case["stimuli_meta_state"]

                test_context._fire_trigger_spy.side_effect = state_machine._fire_trigger
                state_machine._fire_trigger = test_context._fire_trigger_spy

                state_machine.next_state(stimuli)

                self.assertEqual(state_machine.current_state, case["expected_terminal_state"])
                self.assertEqual(state_machine._fire_trigger.mock_calls,
                                 case["expected_get_trigger_calls"])

    def test_from_starting_state_call_correct_actions(self, test_context):
        def create_case(current_state, action):
            return {"current_state": current_state, "action": action}

        cases = [
            create_case(InterpreterState.START, None),
            create_case(InterpreterState.PARSE_TOKENS, self._mock_actions.parse),
            create_case(InterpreterState.DISPATCH_PARSER, self._mock_actions.dispatch),
            create_case(InterpreterState.EVALUATE, self._mock_actions.evaluate),
            create_case(InterpreterState.REPORT_RESULT, self._mock_actions.report)
        ]

        with patch('bbp.state_machine.abstract_state_machine.AbstractStateMachine.current_state', new_callable=PropertyMock) as current_state_property_spy, patch('bbp.message_bus.model.message.Message', autospec=True) as stimuli:
            current_state_property_spy.__set__ = set_property_mock
            stimuli.payload.__set__ = set_property_mock

            for case in cases:
                current_state_property_spy.reset_mock()
                stimuli.reset_mock()
                stimuli.payload.reset_mock()

                self._mock_actions.parse.reset_mock()
                self._mock_actions.dispatch.reset_mock()
                self._mock_actions.evaluate.reset_mock()
                self._mock_actions.report.reset_mock()
                test_context.next_state.reset_mock()

                state_machine = InterpreterStateMachine(
                    test_context.logger, self._mock_actions, self._mock_transition_builder, context_service=test_context.context_service)
                state_machine.current_state = case["current_state"]
                state_machine.next_state = test_context.next_state
                state_machine._frame = test_context.frame

                original_payload = stimuli.payload
                state_machine._on_enter(test_context.previous_state, case["action"], stimuli)

                self.assertEqual(stimuli.meta, case["current_state"])

                if case["current_state"] == InterpreterState.START:
                    self._mock_actions.parse.assert_not_called()
                    self._mock_actions.dispatch.assert_not_called()
                    self._mock_actions.evaluate.assert_not_called()
                    self._mock_actions.report.assert_not_called()
                    state_machine.next_state.assert_not_called()

                elif case["current_state"] == InterpreterState.PARSE_TOKENS:
                    self.assertEqual(case["action"], self._mock_actions.parse)
                    self._mock_actions.parse.assert_called_once_with(original_payload)
                    self.assertEqual(stimuli.payload, self._mock_actions.parse.return_value.value)

                    self._mock_actions.dispatch.assert_not_called()
                    self._mock_actions.evaluate.assert_not_called()
                    self._mock_actions.report.assert_not_called()

                    state_machine.next_state.called_once_with(stimuli)
                elif case["current_state"] == InterpreterState.DISPATCH_PARSER:
                    self._mock_actions.parse.assert_not_called()

                    self.assertEqual(case["action"], self._mock_actions.dispatch)
                    self._mock_actions.dispatch.assert_called_once_with(stimuli)
                    self.assertEqual(stimuli.payload, original_payload)

                    self._mock_actions.evaluate.assert_not_called()
                    self._mock_actions.report.assert_not_called()

                    state_machine.next_state.assert_not_called()
                elif case["current_state"] == InterpreterState.EVALUATE:
                    self._mock_actions.parse.assert_not_called()
                    self._mock_actions.dispatch.assert_not_called()

                    self.assertEqual(case["action"], self._mock_actions.evaluate)
                    self._mock_actions.evaluate.assert_called_once_with(
                        original_payload, test_context.frame)

                    self._mock_actions.report.assert_not_called()
                    state_machine.next_state.called_once_with(stimuli)
                elif case["current_state"] == InterpreterState.REPORT_RESULT:
                    self._mock_actions.parse.assert_not_called()
                    self._mock_actions.dispatch.assert_not_called()
                    self._mock_actions.evaluate.assert_not_called()

                    self.assertEqual(case["action"], self._mock_actions.report)
                    self._mock_actions.report.assert_called_once_with(
                        original_payload, test_context.frame)

                    state_machine.next_state.assert_not_called()
