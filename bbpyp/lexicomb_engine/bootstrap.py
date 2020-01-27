from bbpyp.common.common_ioc_container import CommonIocContainer
from bbpyp.message_bus.message_bus_ioc_container import MessageBusIocContainer
from bbpyp.state_machine import StateMachineIocContainer
from bbpyp.lexical_state_machine import LexicalStateMachineIocContainer
from bbpyp.interpreter_state_machine import InterpreterStateMachineIocContainer
from bbpyp.lexicomb.lexicomb_ioc_container import LexicombIocContainer
from bbpyp.ll_combinator.combinator_ioc_container import CombinatorIocContainer
from bbpyp.lexicomb_engine import LexicombEngineIocContainer


def Bootstrap(app_config, app_main):

    lexicomb_engine_ioc = LexicombEngineIocContainer(
        config=app_config,
        main=app_main,
        common_ioc_factory=CommonIocContainer,
        message_bus_ioc_factory=MessageBusIocContainer,
        combinator_ioc_factory=CombinatorIocContainer,
        lexicomb_ioc_factory=LexicombIocContainer,
        state_machine_ioc_factory=StateMachineIocContainer,
        lexical_state_machine_ioc_factory=LexicalStateMachineIocContainer,
        interpreter_state_machine_ioc_factory=InterpreterStateMachineIocContainer
    )

    return lexicomb_engine_ioc
