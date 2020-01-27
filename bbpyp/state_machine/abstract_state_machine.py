from abc import ABC, abstractmethod

from bbpyp.state_machine.exception.transition_guard_error import TransitionGuardError
from bbpyp.state_machine.exception.transition_guard_warning import TransitionGuardWarning
from bbpyp.state_machine.exception.transition_guard_ignore import TransitionGuardIgnore


class AbstractStateMachine(ABC):

    __CONTEXT_CURRENT_STATE_KEY = "current_state"

    def __init__(self, logger, initial_state, context_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logger
        self._initial_state = initial_state
        self._context_service = context_service

    def next_state(self, stimuli):
        trigger = self._get_trigger(stimuli)
        action, transition_guard, goal_state = self._fire_trigger(trigger)
        self._logger.debug("with stimuli {} given trigger {}, current_state :{}, actions : {}, goal_state : {}",
                           stimuli, trigger, self.current_state, action, goal_state)

        try:
            self.__on_exit(goal_state, transition_guard, stimuli)
            previous_state = self.current_state
            self.current_state = goal_state
            self.__on_enter(previous_state, action, stimuli)
        except (TransitionGuardError, TransitionGuardWarning, TransitionGuardIgnore) as error:
            self.__on_transition_fail(goal_state, stimuli, error)

        self._logger.debug("leaving next_state with current_state = {}", self.current_state)

    def _get_trigger(self, stimuli):
        trigger_parameter = self._get_trigger_parameter(stimuli)
        trigger_state = self.__get_trigger_state(stimuli, trigger_parameter)

        return (self.current_state, trigger_state) if trigger_parameter is None else (
            self.current_state, trigger_state, trigger_parameter)

    def _fire_trigger(self, trigger):
        if trigger not in self._transitions:
            self._logger.debug(
                "could not find trigger {} in transitions {}", trigger, self._transitions)
        return self._transitions[trigger]

    @abstractmethod
    def _get_trigger_state(self, **kwargs):
        pass

    def _get_trigger_parameter(self, stimuli):
        pass

    @property
    @abstractmethod
    def _transitions(self):
        pass

    def __get_trigger_state(self, stimuli, trigger_parameter):
        return self._get_trigger_state(stimuli=stimuli, trigger_parameter=trigger_parameter)

    def __on_exit(self, goal_state, transition_guard, stimuli):
        self._on_exit(goal_state=goal_state, transition_guard=transition_guard, stimuli=stimuli)
        self._logger.debug(
            "transitioning from {} => {} given stimuli ({})", self.current_state, goal_state, stimuli)

    def __on_enter(self, previous_state, action, stimuli):
        self._logger.debug(
            "entered {} from {} with action = {} and stimuli ({})", self.current_state, previous_state, action,  stimuli)
        self._on_enter(previous_state=previous_state, action=action, stimuli=stimuli)

    def __on_transition_fail(self, goal_state, stimuli, fault):
        if isinstance(fault, TransitionGuardError):
            self._logger.error(
                "failed to transition from {} => {} given stimuli ({}) due to: {}", self.current_state, goal_state, stimuli, fault)
        elif isinstance(fault, TransitionGuardWarning):
            self._logger.warn(
                "failed to transition from {} => {} given stimuli ({}) due to: {}", self.current_state, goal_state, stimuli, fault)

        self._on_transition_fail(goal_state=goal_state, stimuli=stimuli, fault=fault)

    def _on_exit(self, **kwargs):
        pass

    @abstractmethod
    def _on_enter(self, **kwargs):
        pass

    def _on_transition_fail(self, **kwargs):
        pass

    @property
    def current_state(self):
        current_state = self._context_service.get_context_variable(
            type(self).__CONTEXT_CURRENT_STATE_KEY)
        if current_state is None:
            self._logger.debug("state context None. setting context variable from getter.")
            self._context_service.set_context_variable(
                type(self).__CONTEXT_CURRENT_STATE_KEY, self._initial_state)

        return self._context_service.get_context_variable(type(self).__CONTEXT_CURRENT_STATE_KEY)

    @current_state.setter
    def current_state(self, state):
        return self._context_service.set_context_variable(type(self).__CONTEXT_CURRENT_STATE_KEY, state)
