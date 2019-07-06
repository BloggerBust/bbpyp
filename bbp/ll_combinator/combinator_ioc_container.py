from dependency_injector import containers, providers
from bbp.ll_combinator.concat import Concat
from bbp.ll_combinator.lhs_or_rhs import LhsOrRhs
from bbp.ll_combinator.defer import Defer
from bbp.ll_combinator.match import Match
from bbp.ll_combinator.repeat_match import RepeatMatch
from bbp.ll_combinator.tag import Tag
from bbp.ll_combinator.reserved import Reserved
from bbp.ll_combinator.apply import Apply
from bbp.ll_combinator.greedy import Greedy
from bbp.ll_combinator.expression import Expression


class CombinatorIocContainer(containers.DeclarativeContainer):
    """Inversion of control container for combinators and parsers"""

    def bootstrap_container(common_ioc):
        CombinatorIocContainer.instance = CombinatorIocContainer(common_ioc=common_ioc)
        return CombinatorIocContainer.instance

    # Dependencies provided by third party packages
    common_ioc = providers.DependenciesContainer()

    # self dependencies
    defer_combinator_provider = providers.Factory(
        lambda: CombinatorIocContainer.instance.defer_combinator_delegated_factory)
    reserved_combinator_provider = providers.Factory(
        lambda: CombinatorIocContainer.instance.reserved_combinator_factory)
    match_combinator_provider = providers.Factory(
        lambda: CombinatorIocContainer.instance.match_combinator_factory)
    repeat_match_combinator_provider = providers.Factory(
        lambda: CombinatorIocContainer.instance.repeat_match_combinator_factory)
    greedy_combinator_provider = providers.Factory(
        lambda: CombinatorIocContainer.instance.greedy_combinator_delegated_factory)

    #factories and delegates
    lhs_or_rhs_combinator_delegated_factory = providers.DelegatedFactory(
        LhsOrRhs, source_format_service=common_ioc.source_format_service_provider, context_service=common_ioc.context_service_provider)
    concat_combinator_delegated_factory = providers.DelegatedFactory(
        Concat, source_format_service=common_ioc.source_format_service_provider, context_service=common_ioc.context_service_provider)
    apply_combinator_delegated_factory = providers.DelegatedFactory(
        Apply, source_format_service=common_ioc.source_format_service_provider, context_service=common_ioc.context_service_provider)

    expression_combinator_factory = providers.DelegatedFactory(
        Expression,
        reserved_factory=reserved_combinator_provider,
        match_factory=match_combinator_provider,
        repeat_match_factory=repeat_match_combinator_provider,
        source_format_service=common_ioc.source_format_service_provider,
        context_service=common_ioc.context_service_provider)

    greedy_combinator_delegated_factory = providers.DelegatedFactory(
        Greedy,
        concat_factory=concat_combinator_delegated_factory,
        lhs_or_rhs_factory=lhs_or_rhs_combinator_delegated_factory,
        expression_factory=expression_combinator_factory,
        apply_factory=apply_combinator_delegated_factory,
        greedy_factory=greedy_combinator_provider,
        defer_factory=defer_combinator_provider,
        source_format_service=common_ioc.source_format_service_provider,
        context_service=common_ioc.context_service_provider)

    match_combinator_factory = providers.DelegatedFactory(
        Match,
        concat_factory=concat_combinator_delegated_factory,
        lhs_or_rhs_factory=lhs_or_rhs_combinator_delegated_factory,
        expression_factory=expression_combinator_factory,
        apply_factory=apply_combinator_delegated_factory,
        greedy_factory=greedy_combinator_delegated_factory,
        defer_factory=defer_combinator_provider,
        source_format_service=common_ioc.source_format_service_provider,
        context_service=common_ioc.context_service_provider)

    repeat_match_combinator_factory = providers.DelegatedFactory(
        RepeatMatch,
        match_factory=match_combinator_factory,
        concat_factory=concat_combinator_delegated_factory,
        lhs_or_rhs_factory=lhs_or_rhs_combinator_delegated_factory,
        expression_factory=expression_combinator_factory,
        apply_factory=apply_combinator_delegated_factory,
        greedy_factory=greedy_combinator_delegated_factory,
        defer_factory=defer_combinator_provider,
        source_format_service=common_ioc.source_format_service_provider,
        context_service=common_ioc.context_service_provider)

    reserved_combinator_factory = providers.DelegatedFactory(
        Reserved,
        concat_factory=concat_combinator_delegated_factory,
        lhs_or_rhs_factory=lhs_or_rhs_combinator_delegated_factory,
        expression_factory=expression_combinator_factory,
        apply_factory=apply_combinator_delegated_factory,
        greedy_factory=greedy_combinator_delegated_factory,
        defer_factory=defer_combinator_provider,
        source_format_service=common_ioc.source_format_service_provider,
        context_service=common_ioc.context_service_provider)

    tag_combinator_factory = providers.DelegatedFactory(
        Tag,
        concat_factory=concat_combinator_delegated_factory,
        lhs_or_rhs_factory=lhs_or_rhs_combinator_delegated_factory,
        expression_factory=expression_combinator_factory,
        apply_factory=apply_combinator_delegated_factory,
        greedy_factory=greedy_combinator_delegated_factory,
        defer_factory=defer_combinator_provider,
        source_format_service=common_ioc.source_format_service_provider,
        context_service=common_ioc.context_service_provider)

    defer_combinator_delegated_factory = providers.DelegatedFactory(
        Defer,
        concat_factory=concat_combinator_delegated_factory,
        lhs_or_rhs_factory=lhs_or_rhs_combinator_delegated_factory,
        expression_factory=expression_combinator_factory,
        apply_factory=apply_combinator_delegated_factory,
        greedy_factory=greedy_combinator_delegated_factory,
        defer_factory=defer_combinator_provider,
        source_format_service=common_ioc.source_format_service_provider,
        context_service=common_ioc.context_service_provider)

    build = providers.Callable(bootstrap_container, common_ioc=common_ioc)
