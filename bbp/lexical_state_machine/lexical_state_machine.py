from bbp.state_machine import AbstractStateMachine
from bbp.lexical_state_machine.model.lexical_state import LexicalState
from bbp.state_machine.exception.transition_guard_ignore import TransitionGuardIgnore


class LexicalStateMachine(AbstractStateMachine):
    def __init__(self, logger, lexical_actions, state_transition_builder, *args, **kwargs):
        super().__init__(logger, LexicalState.START, *args, **kwargs)

        self._actions = lexical_actions
        self._trigger_to_transition = state_transition_builder.from_state(
            LexicalState.START
        ).given_trigger_state(
            LexicalState.PARSE_TAGS
        ).take_transition_action(
            self.actions.tokenize
        ).transition_to_state(
            LexicalState.PARSE_TAGS
        ).append(
        ).from_state(
            LexicalState.DISPATCH_TOKENS
        ).append(
        ).from_state(
            LexicalState.PARSE_TAGS
        ).given_trigger_state(
            LexicalState.DISPATCH_TOKENS
        ).take_transition_action(
            self.actions.dispatch
        ).transition_to_state(
            LexicalState.DISPATCH_TOKENS
        ).provided_guard_is_satisfied(
            self._transition_guard_ignore
        ).build()

    def _on_enter(self, previous_state, action, stimuli, **kwargs):

        stimuli.meta = self.current_state
        if self.current_state == LexicalState.PARSE_TAGS:
            stimuli.payload = action(stimuli.payload)
            self.next_state(stimuli)
        elif self.current_state == LexicalState.DISPATCH_TOKENS:
            action(stimuli)

    def _on_exit(self, transition_guard, stimuli, **kwargs):
        if transition_guard is not None:
            transition_guard(stimuli)

    def _on_transition_fail(self, stimuli, fault, **kwargs):
        if isinstance(fault, TransitionGuardIgnore):
            self._logger.debug("deleting {}", stimuli)
            stimuli.free()
            self.current_state = LexicalState.START

    def _get_trigger_state(self, stimuli, **kwargs):
        trigger = None

        if stimuli.meta == None or stimuli.meta == LexicalState.DISPATCH_TOKENS:
            trigger = LexicalState.PARSE_TAGS
        elif stimuli.meta == LexicalState.PARSE_TAGS:
            trigger = LexicalState.DISPATCH_TOKENS
        else:
            trigger = LexicalState.ERROR_STATE

        self._logger.debug("_get_trigger_state with stimuli = {} returns {}", stimuli, trigger)
        return trigger

    @classmethod
    def _transition_guard_ignore(cls, stimuli):
        if len(stimuli.payload) == 0:
            raise TransitionGuardIgnore("ignoring blank line")

    @property
    def _transitions(self):
        return self._trigger_to_transition

    @property
    def actions(self):
        return self._actions
