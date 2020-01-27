from bbpyp.state_machine.abstract_state_machine import AbstractStateMachine
from bbpyp.interpreter_state_machine.interpreter_state import InterpreterState


class InterpreterStateMachine(AbstractStateMachine):
    def __init__(self, logger, interpreter_actions, state_transition_builder, *args, **kwargs):
        super().__init__(logger, InterpreterState.START, *args, **kwargs)
        self._actions = interpreter_actions

        self._trigger_to_transition = state_transition_builder.from_state(
            InterpreterState.START
        ).given_trigger_state(
            InterpreterState.PARSE_TOKENS
        ).take_transition_action(
            self._actions.parse
        ).transition_to_state(
            InterpreterState.PARSE_TOKENS
        ).append(
        ).from_state(
            InterpreterState.DISPATCH_PARSER
        ).append(
        ).from_state(
            InterpreterState.PARSE_TOKENS
        ).given_trigger_state(
            InterpreterState.DISPATCH_PARSER
        ).take_transition_action(
            self._actions.dispatch
        ).transition_to_state(
            InterpreterState.DISPATCH_PARSER
        ).append(
        ).from_state(
            InterpreterState.START
        ).given_trigger_state(
            InterpreterState.EVALUATE
        ).take_transition_action(
            self._actions.evaluate
        ).transition_to_state(
            InterpreterState.EVALUATE
        ).append(
        ).from_state(
            InterpreterState.REPORT_RESULT
        ).append(
        ).from_state(
            InterpreterState.EVALUATE
        ).given_trigger_state(
            InterpreterState.REPORT_RESULT
        ).take_transition_action(
            self._actions.report
        ).transition_to_state(
            InterpreterState.REPORT_RESULT
        ).build()

        self._frame = {}

    def _on_enter(self, previous_state, action, stimuli, **kwargs):
        stimuli.meta = self.current_state
        if self.current_state == InterpreterState.PARSE_TOKENS:
            self._logger.debug("parsing stimuli: {}", stimuli)
            result = action(stimuli.payload)
            self._logger.debug(
                "parsed stimuli payload: {} of type {}", result.value, type(result.value))
            stimuli.payload = result.value
            self.next_state(stimuli)
        elif self.current_state == InterpreterState.DISPATCH_PARSER:
            self._logger.debug("dispatching stimuli sequence: {}", stimuli.sequence_number)

            action(stimuli)
        elif self.current_state == InterpreterState.EVALUATE:
            self._logger.debug(
                "evaluating stimuli: {} with payload type {}", stimuli, (stimuli.payload))
            result = action(stimuli.payload, self._frame)
            self._logger.debug("[{}] result = {}", self, result)
            self.next_state(stimuli)
        elif self.current_state == InterpreterState.REPORT_RESULT:
            action(stimuli.payload, self._frame)

    def _get_trigger_state(self, stimuli, **kwargs):
        trigger = None

        if stimuli.meta == InterpreterState.PARSE_TOKENS:
            trigger = InterpreterState.DISPATCH_PARSER
        elif stimuli.meta == InterpreterState.DISPATCH_PARSER:
            trigger = InterpreterState.EVALUATE
        elif stimuli.meta == InterpreterState.EVALUATE:
            trigger = InterpreterState.REPORT_RESULT
        else:
            trigger = InterpreterState.PARSE_TOKENS

        return trigger

    @property
    def _transitions(self):
        return self._trigger_to_transition

    @property
    def actions(self):
        return self._actions
