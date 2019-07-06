class StateTransitionBuilder:

    def __init__(self, trigger_transition_factory):

        self._trigger_transition_factory = trigger_transition_factory

        self._from_state = None
        self._trigger_state = None
        self._trigger_parameter = None

        self._transition_action = None
        self._transition_guard = None
        self._transition_state = None

        self._transitions = dict()

    def from_state(self, from_state):
        self._from_state = from_state
        return self

    def given_trigger_state(self, trigger_state):
        self._trigger_state = trigger_state
        return self

    def with_trigger_parameter(self, trigger_parameter):
        self._trigger_parameter = trigger_parameter
        return self

    def take_transition_action(self, transition_action):
        self._transition_action = transition_action
        return self

    def provided_guard_is_satisfied(self, transition_guard):
        self._transition_guard = transition_guard
        return self

    def without_guard(self):
        self._transition_guard = None
        return self

    def transition_to_state(self, transition_state):
        self._transition_state = transition_state
        return self

    def append(self):
        trigger = (self._from_state, self._trigger_state, self._trigger_parameter) if self._trigger_parameter else (
            self._from_state, self._trigger_state,)

        trigger_transition = self._trigger_transition_factory(trigger, (
            self._transition_action, self._transition_guard, self._transition_state))

        self._transitions[trigger_transition.trigger] = trigger_transition.transition
        return self

    def build(self):
        self.append()
        return self._transitions.copy()
