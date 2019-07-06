import logging
from dependency_injector import containers, providers

from bbp.common.util.ioc_util import IocUtil
from bbp.tag_script.lexer.model.tag_expressions import TagExpressions
from bbp.tag_script.lexer.tag_expressions_builder import TagExpressionsBuilder
from bbp.tag_script.lexer.lexer import Lexer
from bbp.tag_script.parser.model.result import Result
from bbp.tag_script.parser.no_op_statement import NoOpStatement
from bbp.tag_script.parser.variable import Variable
from bbp.tag_script.parser.real_number import RealNumber
from bbp.tag_script.parser.string import String
from bbp.tag_script.parser.hash import Hash
from bbp.tag_script.parser.access import Access
from bbp.tag_script.parser.assignment import Assignment
from bbp.tag_script.parser.block import Block
from bbp.tag_script.parser.return_statement import ReturnStatement
from bbp.tag_script.parser.exist import Exist
from bbp.tag_script.parser.conditional import Conditional
from bbp.tag_script.parser.conditional_repeat import ConditionalRepeat
from bbp.tag_script.parser.unary_operator_factory import UnaryOperatorFactory
from bbp.tag_script.parser.logical_unary_operator import LogicalUnaryOperator
from bbp.tag_script.parser.arethmatic_unary_operator import ArethmaticUnaryOperator
from bbp.tag_script.parser.binary_operator_factory import BinaryOperatorFactory
from bbp.tag_script.parser.arethmatic_binary_operator import ArethmaticBinaryOperator
from bbp.tag_script.parser.relational_binary_operator import RelationalBinaryOperator
from bbp.tag_script.parser.logical_binary_operator import LogicalBinaryOperator
from bbp.tag_script.parser.select_operator_factory import SelectOperatorFactory
from bbp.tag_script.parser.tag_statement import TagStatement
from bbp.tag_script.parser.parser import Parser


class TagScriptIocContainer(containers.DeclarativeContainer):
    """Inversion of control container for the TagScript parser"""

    def bootstrap_container(config, logger, common_ioc, combinator_ioc, *args, **kwargs):

        TagScriptIocContainer.instance = TagScriptIocContainer(
            config=config, common_ioc=common_ioc, combinator_ioc=combinator_ioc)
        IocUtil.identify_singletons_to_be_skipped_during_deepcopy(TagScriptIocContainer.instance)

        return TagScriptIocContainer.instance

    common_ioc = providers.DependenciesContainer()
    combinator_ioc = providers.DependenciesContainer()

    # Configuration
    config = providers.Configuration('config')
    config_provider = providers.Object(config)
    logging_provider = IocUtil.create_basic_log_adapter(providers, "tag_script")

    # internal providers
    parser_factory_provider = providers.Singleton(
        lambda: TagScriptIocContainer.instance.parser_provider())

    src_provider = providers.Singleton(
        lambda: TagScriptIocContainer.instance.config.tag_script.src())

    # lexer
    tag_exprssions_factory = providers.DelegatedFactory(TagExpressions)
    tag_expressions_builder_factory = providers.Factory(
        TagExpressionsBuilder, tag_expressions_factory=tag_exprssions_factory)

    # parser
    result_factory_provider = providers.DelegatedFactory(Result)
    variable_provider = providers.DelegatedFactory(Variable, result_factory=result_factory_provider)
    real_number_factory_provider = providers.DelegatedFactory(
        RealNumber, result_factory=result_factory_provider)
    string_factory_provider = providers.DelegatedFactory(
        String, result_factory=result_factory_provider)
    hash_provider = providers.DelegatedFactory(Hash, result_factory=result_factory_provider)
    access_provider = providers.DelegatedFactory(Access, result_factory=result_factory_provider)
    assignment_provider = providers.DelegatedFactory(
        Assignment, result_factory=result_factory_provider)
    block_factory_provider = providers.DelegatedFactory(
        Block, result_factory=result_factory_provider)
    return_statement_factory_provider = providers.DelegatedFactory(
        ReturnStatement, result_factory=result_factory_provider)
    exist_provider = providers.DelegatedFactory(Exist, result_factory=result_factory_provider)
    conditional_provider = providers.DelegatedFactory(
        Conditional, result_factory=result_factory_provider)
    conditional_repeat_provider = providers.DelegatedFactory(
        ConditionalRepeat, result_factory=result_factory_provider)

    logical_unary_operator_provider = providers.DelegatedFactory(
        LogicalUnaryOperator, result_factory=result_factory_provider)
    arethmatic_unary_operator_provider = providers.DelegatedFactory(
        ArethmaticUnaryOperator, result_factory=result_factory_provider)
    unary_operator_factory = providers.Factory(
        UnaryOperatorFactory, logical_unary_operator_factory=logical_unary_operator_provider, arethmatic_unary_operator_factory=arethmatic_unary_operator_provider)

    arethmatic_binary_operator_provider = providers.DelegatedFactory(
        ArethmaticBinaryOperator, real_number_factory=real_number_factory_provider, string_factory=string_factory_provider, result_factory=result_factory_provider)
    relational_binary_operator_provider = providers.DelegatedFactory(
        RelationalBinaryOperator, result_factory=result_factory_provider)
    logical_binary_operator_provider = providers.DelegatedFactory(
        LogicalBinaryOperator, result_factory=result_factory_provider)

    binary_operator_factory = providers.Factory(BinaryOperatorFactory, arethmatic_binary_operator_factory=arethmatic_binary_operator_provider,
                                                relational_binary_operator_factory=relational_binary_operator_provider, logical_binary_operator_factory=logical_binary_operator_provider)

    select_operator_factory = providers.Factory(
        SelectOperatorFactory, unary_operator_factory=unary_operator_factory, binary_operator_factory=binary_operator_factory)

    # Delegates for consumer's of this package
    lexer_provider = providers.Singleton(
        Lexer, logger=logging_provider, tag_expressions_builder=tag_expressions_builder_factory)

    tag_statement_provider = providers.DelegatedFactory(
        TagStatement, parser_service=parser_factory_provider, lexer_service=lexer_provider, scripts_path=src_provider, file_stream_service=common_ioc.file_stream_service_provider, result_factory=result_factory_provider)

    no_op_statement_factory_provider = providers.DelegatedFactory(
        NoOpStatement, result_factory=result_factory_provider)

    parser_provider = providers.Singleton(
        Parser,
        logger=logging_provider,
        tag_factory=combinator_ioc.tag_combinator_factory.delegate(),
        reserved_factory=combinator_ioc.reserved_combinator_factory.delegate(),
        repeat_match_factory=combinator_ioc.repeat_match_combinator_factory.delegate(),
        variable_factory=variable_provider,
        real_number_factory=real_number_factory_provider,
        hash_factory=hash_provider,
        access_factory=access_provider,
        unary_operator_factory=unary_operator_factory,
        binary_operator_factory=binary_operator_factory,
        select_operator_factory=select_operator_factory,
        assignment_factory=assignment_provider,
        block_factory=block_factory_provider,
        return_statement_factory=return_statement_factory_provider,
        no_op_statement_factory=no_op_statement_factory_provider,
        exist_factory=exist_provider,
        conditional_factory=conditional_provider,
        conditional_repeat_factory=conditional_repeat_provider,
        tag_statement_factory=tag_statement_provider,

        source_format_service=common_ioc.source_format_service_provider,
        context_service=common_ioc.context_service_provider,
    )

    build = providers.Callable(bootstrap_container, config=config_provider,
                               logger=logging_provider, common_ioc=common_ioc, combinator_ioc=combinator_ioc)
