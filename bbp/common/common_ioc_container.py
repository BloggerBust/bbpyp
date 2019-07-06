import logging
from pathlib import Path
from io import open as synchronous_open_file
from dependency_injector import containers, providers

from bbp.common.log.basic_log_adapter import BasicLogAdapter
from bbp.common.log.message import Message
from bbp.common.log.basic_context_filter import BasicContextFilter
from bbp.common.service.source_format_service import SourceFormatService
from bbp.common.service.context_service import ContextService
from bbp.common.service.action_context_manager import ActionContextManager
from bbp.common.service.async_service import AsyncService
from bbp.common.service.notification_service import NotificationService
from bbp.common.service.sequence_service import SequenceService
from bbp.common.service.file_stream_service import FileStreamService
from bbp.common.service.named_item_service import NamedItemService
from bbp.common.service.metric_service import MetricService
from bbp.common.service.queue_service import QueueService
from bbp.common.model.fifo_queue import FifoQueue
from bbp.common.model.sequence_queue import SequenceQueue
from bbp.common.model.queue_factory import QueueFactory
from bbp.common.model.sequential_transfer_object import SequentialTransferObject
from bbp.common.model.link_node_iter import LinkNodeIter
from bbp.common.model.single_link_node import SingleLinkNode
from bbp.common.model.singly_linked_list import SinglyLinkedList
from bbp.common.util.ioc_util import IocUtil


class CommonIocContainer(containers.DeclarativeContainer):

    def bootstrap_container(config, source_format_rules, configure_logger, logger):
        CommonIocContainer.instance = CommonIocContainer(
            config=config, source_format_rules=source_format_rules)

        container = CommonIocContainer.instance
        IocUtil.identify_singletons_to_be_skipped_during_deepcopy(container)
        logger.info("common container configuration complete")
        return CommonIocContainer.instance

    # Configuration
    config = providers.Configuration('config')
    source_format_rules = providers.Configuration('source_format_rules')

    config_provider = providers.Object(config)
    configure_logger = providers.Callable(logging.config.dictConfig, config.logger)
    logging_provider = IocUtil.create_basic_log_adapter(providers, "common")

    source_format_service_provider = providers.Singleton(
        SourceFormatService, format_rules=source_format_rules)

    context_service_provider = providers.Singleton(ContextService)
    context_filter_provider = providers.Singleton(
        BasicContextFilter, context_service=context_service_provider)

    action_context_factory_provider = providers.DelegatedFactory(
        ActionContextManager, context_service=context_service_provider)

    async_service_provider = providers.Singleton(
        AsyncService,
        logger=logging_provider,
        context_service=context_service_provider,
        action_context_factory=action_context_factory_provider,
        memory_channel_max_buffer_size=config.memory_channel_max_buffer_size)

    named_item_service_provider = providers.Factory(NamedItemService)

    notification_service_provider = providers.Singleton(
        NotificationService,
        logger=logging_provider,
        named_item_service=named_item_service_provider,
        async_service=async_service_provider)

    path_service_provider = providers.DelegatedFactory(Path)
    open_file_service_provider = providers.DelegatedFactory(synchronous_open_file)

    file_stream_service_provider = providers.Singleton(
        FileStreamService,
        logger=logging_provider,
        async_service=async_service_provider,
        open_file_service=open_file_service_provider,
        path_service=path_service_provider,
        context_service=context_service_provider,
    )

    metric_service_provider = providers.Singleton(
        MetricService, named_item_service=named_item_service_provider)

    fifo_queue_provider = providers.DelegatedFactory(FifoQueue)
    sequence_service_provider = providers.Singleton(
        SequenceService, fifo_queue_factory=fifo_queue_provider, named_item_service=named_item_service_provider)

    sequence_queue_provider = providers.DelegatedFactory(
        SequenceQueue, sequence_service=sequence_service_provider)
    queue_factory_provider = providers.Factory(
        QueueFactory, fifo_queue_factory=fifo_queue_provider, sequence_queue_factory=sequence_queue_provider)
    queue_service_provider = providers.Singleton(
        QueueService, named_item_service=named_item_service_provider, queue_factory=queue_factory_provider, metric_service=metric_service_provider)

    sequential_transfer_object_provider = providers.DelegatedFactory(
        SequentialTransferObject, sequence_service=sequence_service_provider)

    link_node_iter_delegated_factory = providers.DelegatedFactory(LinkNodeIter)
    single_link_node_delegated_factory = providers.DelegatedFactory(
        SingleLinkNode, link_node_iter_factory=link_node_iter_delegated_factory)
    singly_linked_list_factory = providers.Factory(
        SinglyLinkedList, single_link_node_factory=single_link_node_delegated_factory)

    build = providers.Callable(bootstrap_container, config=config_provider, source_format_rules=source_format_rules,
                               configure_logger=configure_logger, logger=logging_provider)
