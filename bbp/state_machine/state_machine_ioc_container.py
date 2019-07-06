from dependency_injector import containers, providers

from bbp.state_machine.model.trigger_transition import TriggerTransition
from bbp.state_machine.state_transition_builder import StateTransitionBuilder

class StateMachineIocContainer(containers.DeclarativeContainer):
    trigger_transition_factory = providers.DelegatedFactory(TriggerTransition)

    # Delegates for consumer's of this package
    state_transition_builder_factory = providers.Factory(
        StateTransitionBuilder, trigger_transition_factory=trigger_transition_factory)
