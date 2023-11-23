from typing import Any

from query_builder.filtering.configurations import (
    default_filters_config,
)
from query_builder.filtering.models import (
    AbstractFilterRule,
    CompilationConfig,
)
from query_builder.filtering.models.conditions import Conditions
from query_builder.filtering.models.rules import ComplexFilterRule, SimpleFilterRule
from query_builder.shared.models import FieldMap, CompilationContext


def apply_filters(
    filters: AbstractFilterRule | None,
    fields_map: list[FieldMap],
    *queries,
    config: CompilationConfig = None,
    statement: Any | None = None,
) -> tuple:
    """
    Parse the filters and build the SQL where statement to append
    to the given SqlAlchemy queries. If a statement is provided, it will be used instead of parsing the filters.

    :param filters: the filters to build.
    :param fields_map: the mapping between the 'field' inside the filter and the SqlAlchemy Column.
    :param queries: the queries to process.
    :param config: configuration to use to parse the filters.
    :param statement: WHERE statement to use instead of parsing the filters.
    :return: the queries with the filters applied.
    """
    if not filters:
        return tuple(queries)

    context = CompilationContext()
    if not statement:
        statement, _ = build_filters(filters, fields_map, context, config)
    return tuple([query.where(statement).params(context.params) for query in queries])


def build_filters(
    filters: AbstractFilterRule,
    fields_map: list[FieldMap],
    context: CompilationContext,
    config: CompilationConfig = None,
) -> tuple[Any, CompilationContext]:
    """
    Parse the filters and build the corresponding SQL where statement.
    Also returns the list of fields that appear in the filters.

    :param filters: the filters to build.
    :param fields_map: the mapping between the 'field' inside the filter and the SqlAlchemy Column.
    :param context: the compilation context to use. Contains parameters and internals of the compilation.
    :param config: configuration to use to parse the filters.
    :return: the WHERE statement and the set of included fields.
    """
    config = config or default_filters_config(fields_map)
    statement = filters.compile(config, context)
    return statement, context


def try_parse_dict(
    filters: dict, *, syntax_types: list[type[AbstractFilterRule]] = None
) -> AbstractFilterRule:
    """
    Try to parse the filters.

    :param filters: the filters to parse.
    :param syntax_types: the syntax types to use to parse the filters.
    :return: the AbstractFilterRule object parsed from the input.
    """
    syntax_types = syntax_types or [ComplexFilterRule, SimpleFilterRule]
    for syntax_type in syntax_types:
        rule = syntax_type.try_parse_dict(filters)
        if rule:
            return rule


def join_filters(
    *filters: AbstractFilterRule, condition: str = Conditions.AND.value
) -> AbstractFilterRule | None:
    """
    Join the given filters using the given condition.

    :param filters: the filters to join.
    :param condition: the condition to use to join the filters.
    :return: the joined filter.
    """
    filters = [f for f in filters if f]
    if not filters:
        return None
    if len(filters) == 1:
        return filters[0]
    return ComplexFilterRule(condition, list(filters))
