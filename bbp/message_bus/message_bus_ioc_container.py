import logging
import logging.config
from dependency_injector import containers, providers

from bbp.common.model.queue_type import QueueType
from bbp.common.util.ioc_util import IocUtil
from bbp.message_bus.pub_sub import PubSub
from bbp.message_bus.model.bus import Bus
from bbp.message_bus.model.topic_channel import TopicChannel
from bbp.message_bus.model.message import Message
from bbp.message_bus.model.message_pipe import MessagePipe
from bbp.message_bus.message_pipe_line_builder import MessagePipeLineBuilder


def bootstrap_container(config, common_ioc, configure_logger, logger):
    context_filter = common_ioc.context_filter_provider()
    logger.logger.addFilter(context_filter)
    MessageBusIocContainer.instance = MessageBusIocContainer(
        config=config, common_ioc=common_ioc)
    container = MessageBusIocContainer.instance

    if not container.config.memory_channel_topic_default():
        container.config.memory_channel_topic_default.update({
            "publish_concurrency": 0,
            "subscribe_concurrency": 0,
            "subscribe_queue_type": QueueType.FIFO
        })

    IocUtil.identify_singletons_to_be_skipped_during_deepcopy(container)
    logger.info("container configuration complete")
    return MessageBusIocContainer.instance


class MessageBusIocContainer(containers.DeclarativeContainer):

    common_ioc = providers.DependenciesContainer()

    # Configuration
    config = providers.Configuration('config')
    configure_logger = providers.Callable(logging.config.dictConfig, config.logger)
    config_provider = providers.Object(config)
    logging_provider = IocUtil.create_basic_log_adapter(
        providers, "message_bus", extra={"CONTEXT_ID": None})

    # Internal Providers
    message_bus_factory_provider = providers.Factory(
        lambda: MessageBusIocContainer.instance.message_bus_factory.delegate)

    memory_channel_topic_default_provider = providers.Factory(
        config.memory_channel_topic_default)

    # Delegates for consumer's of this package
    message_factory_provider = providers.DelegatedFactory(
        Message, logger=logging_provider, sequence_service=common_ioc.sequence_service_provider)

    topic_channel_delegated_factory = providers.DelegatedFactory(
        TopicChannel,
        logger=logging_provider,
        channel_topic_config=config.memory_channel_topic,
        channel_topic_config_default=memory_channel_topic_default_provider,
        async_service=common_ioc.async_service_provider,
        context_service=common_ioc.context_service_provider)

    message_bus_factory = providers.DelegatedFactory(
        Bus,
        logger=logging_provider,
        bus_factory=message_bus_factory_provider,
        single_link_node_factory=common_ioc.single_link_node_delegated_factory.provider,
        topic_channel_factory=topic_channel_delegated_factory,
        async_service=common_ioc.async_service_provider,
        context_service=common_ioc.context_service_provider)

    message_pipe_delegated_factory = providers.DelegatedFactory(MessagePipe)
    message_pipe_line_builder_provider = providers.Factory(
        MessagePipeLineBuilder,
        message_pipe_factory=message_pipe_delegated_factory,
        linked_list=common_ioc.singly_linked_list_factory
    )

    pub_sub_provider = providers.Singleton(
        PubSub,
        logger=logging_provider,
        linked_list=common_ioc.singly_linked_list_factory,
        bus_factory=message_bus_factory,
        async_service=common_ioc.async_service_provider,
        context_service=common_ioc.context_service_provider)

    build = providers.Callable(bootstrap_container, config=config_provider,
                               common_ioc=common_ioc, configure_logger=configure_logger, logger=logging_provider)
