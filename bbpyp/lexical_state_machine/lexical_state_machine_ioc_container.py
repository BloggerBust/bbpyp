import logging
import logging.config
from dependency_injector import containers, providers

from bbpyp.common.util.ioc_util import IocUtil
from bbpyp.lexical_state_machine.lexical_state_machine import LexicalStateMachine


class LexicalStateMachineIocContainer(containers.DeclarativeContainer):

    def bootstrap_container(config, logger, common_ioc, state_machine_ioc):

        context_filter = common_ioc.context_filter_provider()
        logger.logger.addFilter(context_filter)
        LexicalStateMachineIocContainer.instance = LexicalStateMachineIocContainer(
            config=config, common_ioc=common_ioc, state_machine_ioc=state_machine_ioc)

        IocUtil.identify_singletons_to_be_skipped_during_deepcopy(
            LexicalStateMachineIocContainer.instance)

        logger.info("container configuration complete")
        return LexicalStateMachineIocContainer.instance

    common_ioc = providers.DependenciesContainer()
    state_machine_ioc = providers.DependenciesContainer()

    # Configuration
    config = providers.Configuration('config')
    logging_provider = IocUtil.create_basic_log_adapter(
        providers, "bbpyp.lexical_state_machine", extra={"CONTEXT_ID": None})

    # Dependencies provided by third party packages
    lexical_actions_provider = providers.Dependency()

    # Delegates for consumer's of this package
    lexical_state_machine_provider = providers.Singleton(
        LexicalStateMachine, logger=logging_provider, lexical_actions=lexical_actions_provider, state_transition_builder=state_machine_ioc.state_transition_builder_factory, context_service=common_ioc.context_service_provider)

    build = providers.Callable(bootstrap_container, config=config,
                               logger=logging_provider, common_ioc=common_ioc, state_machine_ioc=state_machine_ioc)
