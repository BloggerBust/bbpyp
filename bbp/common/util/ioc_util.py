import inspect
import logging
from dependency_injector import providers
from bbp.common.util.collection_util import CollectionUtil
from bbp.common.log.message import Message
from bbp.common.log.basic_log_adapter import BasicLogAdapter


class IocUtil:

    @staticmethod
    def accumulate_registered_singleton_types(container, singleton_types):
        provider_collection = container.providers

        for provider in provider_collection:
            if isinstance(container, providers.DependenciesContainer):
                continue

            provider_instance = container.__dict__[provider]
            provider_type = type(provider_instance)

            if issubclass(provider_type, providers.Singleton) and inspect.isclass(provider_instance.cls):
                CollectionUtil.add_items(singleton_types, provider_instance.cls)

    @staticmethod
    def identify_singletons_to_be_skipped_during_deepcopy(container):
        registered_singleton_types = set()
        IocUtil.accumulate_registered_singleton_types(container, registered_singleton_types)
        CollectionUtil.add_types_to_deepcopy_direct_assignment_list(*registered_singleton_types)

    @staticmethod
    def create_basic_log_adapter(providers, name, extra=None):
        log_message_factory_provider = providers.DelegatedFactory(Message)
        return providers.Singleton(BasicLogAdapter, providers.Singleton(
            logging.getLogger, name=name), log_message_factory=log_message_factory_provider, extra=extra)
