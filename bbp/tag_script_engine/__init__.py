import logging
from os import linesep
from dependency_injector import containers, providers

from bbp.common.util.ioc_util import IocUtil
from bbp.abstract_parser.model.indent_delta import IndentDelta
from bbp.tag_script_engine.model.topic import Topic
from bbp.tag_script_engine.lexical_actions import LexicalActions
from bbp.tag_script_engine.interpreter_actions import InterpreterActions
from bbp.tag_script_engine.tag_script_pub_sub_client import TagScriptPubSubClient


class TagScriptEngineIocContainer:
    instance = None

    class __TagScriptEngineIocContainer:
        def __init__(self, config, main, common_ioc_factory, message_bus_ioc_factory, combinator_ioc_factory, tag_script_ioc_factory, state_machine_ioc_factory, lexical_state_machine_ioc_factory, interpreter_state_machine_ioc_factory):

            self.__instance = containers.DynamicContainer()
            config_provider = providers.Object(config)
            logging_provider = IocUtil.create_basic_log_adapter(providers, "tag_script_engine")
            common_ioc = common_ioc_factory(config=config, source_format_rules={
                ":=": {"format": [(r"\s*{}\s*", r"{} ")]},
                "+": {"format": [(r"\s*{}\s*", r" {} ")]},
                "-": {"format": [(r"\s*{}\s*", r" {} ")]},
                "*": {"format": [(r"\s*{}\s*", r" {} ")]},
                "/": {"format": [(r"\s*{}\s*", r" {} ")]},
                ";": {"format": [(r"\s*{}\s*", r"{}" + linesep)]},
                "{": {"format": [(r"\s*{}\s*", r"{}" + linesep)], "indent_delta": IndentDelta.INCREASE},
                "}": {"format": [(rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{}" + linesep)], "indent_delta": IndentDelta.DECREASE},
                "return": {"format": [(rf"\s*{linesep}{{{{1}}}}(\s*){{}}\s*", linesep + r"\1{} ")]}
            }).build()

            message_bus_ioc = message_bus_ioc_factory(
                config=config,
                common_ioc=common_ioc).build()
            combinator_ioc = combinator_ioc_factory(
                common_ioc=common_ioc).build()
            tag_script_ioc = tag_script_ioc_factory(
                config=config,
                common_ioc=common_ioc,
                combinator_ioc=combinator_ioc).build()
            state_machine_ioc = state_machine_ioc_factory()
            lexical_state_machine_ioc = lexical_state_machine_ioc_factory(
                config=config,
                common_ioc=common_ioc,
                state_machine_ioc=state_machine_ioc).build()
            interpreter_state_machine_ioc = interpreter_state_machine_ioc_factory(
                config=config,
                common_ioc=common_ioc,
                state_machine_ioc=state_machine_ioc).build()

            lexical_actions_provider = providers.Singleton(
                LexicalActions,
                logger=logging_provider,
                lexer=tag_script_ioc.lexer_provider,
                queue_service=common_ioc.queue_service_provider,
                notification_service=common_ioc.notification_service_provider)

            interpreter_actions_provider = providers.Singleton(
                InterpreterActions,
                logger=logging_provider,
                parser_combinator=tag_script_ioc.parser_provider,
                queue_service=common_ioc.queue_service_provider,
                notification_service=common_ioc.notification_service_provider)

            lexical_state_machine_ioc.lexical_actions_provider.provided_by(
                lexical_actions_provider)

            interpreter_state_machine_ioc.interpreter_actions_provider.provided_by(
                interpreter_actions_provider)

            tag_script_pub_sub_client_provider = providers.DelegatedFactory(
                TagScriptPubSubClient,
                logger=logging_provider,
                queue_service=common_ioc.queue_service_provider,
                notification_service=common_ioc.notification_service_provider,
                message_factory=message_bus_ioc.message_factory_provider,
                file_stream_service=common_ioc.file_stream_service_provider,
                context_service=common_ioc.context_service_provider,
                async_service=common_ioc.async_service_provider)

            create_client = providers.DelegatedCallable(
                self.__create_tag_script_client,
                logger=logging_provider,
                pub_sub=message_bus_ioc.pub_sub_provider,
                message_pipe_line_builder=message_bus_ioc.message_pipe_line_builder_provider,
                pub_sub_client_factory=tag_script_pub_sub_client_provider,
                lexical_state_machine=lexical_state_machine_ioc.lexical_state_machine_provider,
                interpreter_state_machine=interpreter_state_machine_ioc.interpreter_state_machine_provider)

            self.__instance.tag_script_ioc = tag_script_ioc

            self.__instance.main = providers.Callable(
                main, create_client=create_client, pub_sub=message_bus_ioc.pub_sub_provider, async_service=common_ioc.async_service_provider, metric_service=common_ioc.metric_service_provider)

        def __create_tag_script_client(self, logger, pub_sub, message_pipe_line_builder, pub_sub_client_factory, tag_stream_src, lexical_state_machine, interpreter_state_machine):

            pub_sub_client = pub_sub_client_factory(tag_stream_src)
            pub_sub.register_topic_publisher(
                Topic.LEXICAL.value, pub_sub_client)
            pub_sub.register_topic_subscriber(
                Topic.LEXICAL.value, pub_sub_client, state_machine=lexical_state_machine)

            pipe_line = message_pipe_line_builder.for_topic(
                Topic.PARSE.value
            ).with_publisher(
                pub_sub_client
            ).with_subscriber(
                pub_sub_client, state_machine=interpreter_state_machine
            ).append_pipe(
            ).for_topic(
                Topic.EVALUATE.value
            ).with_publisher(
                pub_sub_client
            ).with_subscriber(
                pub_sub_client, state_machine=interpreter_state_machine
            ).append_pipe(
            ).for_topic(
                Topic.REPORT.value
            ).with_publisher(
                pub_sub_client
            ).with_subscriber(
                pub_sub_client, state_machine=interpreter_state_machine
            ).build()

            pub_sub.register_message_pipeline(pipe_line)

            return pub_sub_client

        @property
        def main(self):
            return self.__instance.main

        # temporary. Once all the ioc containers are dynamic singletons I can get rid of this.
        @property
        def tag_script_ioc(self):
            return self.__instance.tag_script_ioc

    def __new__(cls, *args, **kwargs):
        if not TagScriptEngineIocContainer.instance:
            TagScriptEngineIocContainer.instance = TagScriptEngineIocContainer.__TagScriptEngineIocContainer(
                *args, **kwargs)
        return TagScriptEngineIocContainer.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
