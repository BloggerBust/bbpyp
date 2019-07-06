from bbp.state_machine.exception.trigger_value_error import TriggerValueError
from bbp.state_machine.exception.transition_value_error import TransitionValueError


class TriggerTransition:
    def __init__(self, trigger, transition):
        if not isinstance(trigger, tuple) or len(trigger) < 2 or len(trigger) > 3:
            raise TriggerValueError("trigger", trigger,
                                    "Trigger must be a tuple of length 2 or 3")

        if not all(trigger):
            raise TriggerValueError("trigger", trigger,
                                    "Trigger must not contain empty, 0 or None elements")

        if not isinstance(transition, tuple) or len(transition) != 3:
            raise TransitionValueError("transition", transition,
                                       "Transition's must be a tupple of length 3")

        self._trigger = trigger
        self._transition = transition

    @property
    def transition(self):
        return self._transition

    @property
    def trigger(self):
        return self._trigger
