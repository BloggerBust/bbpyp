from bbp.common.common_ioc_container import CommonIocContainer
from bbp.message_bus.message_bus_ioc_container import MessageBusIocContainer
from bbp.state_machine import StateMachineIocContainer
from bbp.lexical_state_machine import LexicalStateMachineIocContainer
from bbp.interpreter_state_machine import InterpreterStateMachineIocContainer
from bbp.tag_script.tag_script_ioc_container import TagScriptIocContainer
from bbp.ll_combinator.combinator_ioc_container import CombinatorIocContainer
from bbp.tag_script_engine import TagScriptEngineIocContainer


def Bootstrap(app_config, app_main):

    tag_script_engine_ioc = TagScriptEngineIocContainer(
        config=app_config,
        main=app_main,
        common_ioc_factory=CommonIocContainer,
        message_bus_ioc_factory=MessageBusIocContainer,
        combinator_ioc_factory=CombinatorIocContainer,
        tag_script_ioc_factory=TagScriptIocContainer,
        state_machine_ioc_factory=StateMachineIocContainer,
        lexical_state_machine_ioc_factory=LexicalStateMachineIocContainer,
        interpreter_state_machine_ioc_factory=InterpreterStateMachineIocContainer
    )

    return tag_script_engine_ioc
