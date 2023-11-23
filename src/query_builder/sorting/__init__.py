from query_builder.shared.models import FieldMap, CompilationContext
from query_builder.sorting.configurations import (
    default_sort_config,
)
from query_builder.sorting.errors import QueryBuilderSortSyntaxError
from query_builder.sorting.models import CompilationConfig, AbstractSortRule
from query_builder.sorting.models.rules import SortRule


def apply_sorting(
    sorting_rules: list[AbstractSortRule] | None,
    fields_map: list[FieldMap],
    *queries,
    config: CompilationConfig = None,
    statements: list | None = None,
) -> tuple:
    """
    Parse the sorting rules and build the SQL order by statement to append
    to the given SqlAlchemy queries.

    :param sorting_rules: The sort rules to build.
    :param fields_map: The mapping between the 'field' inside the rule and the SqlAlchemy Column.
    :param queries: The SqlAlchemy queries to process.
    :param config: The configuration to use to parse the rules.
    :param statements: ORDER BY statements to use instead of parsing the rules.
    :return: The SqlAlchemy queries with the sort applied.
    """
    if not sorting_rules:
        return tuple(queries)
    if not isinstance(sorting_rules, list):
        raise QueryBuilderSortSyntaxError("Sort rules must be a list")

    context = CompilationContext()
    if statements is None:
        statements, _ = build_sorting(sorting_rules, fields_map, context, config)
    return tuple([query.order_by(*statements) for query in queries])


def build_sorting(
    sorting_rules: list[AbstractSortRule],
    fields_map: list[FieldMap],
    context: CompilationContext,
    config: CompilationConfig = None,
) -> tuple[list, CompilationContext]:
    """
    Parse the sorting rules and build the corresponding SQL order by statement.

    :param sorting_rules: the sorting rules to build.
    :param fields_map: the mapping between the 'field' inside the rule and the SqlAlchemy Column.
    :param context: the compilation context to use. Contains parameters and internals of the compilation.
    :param config: the configuration to use to parse the rules.
    :return: the order by statement.
    """
    config = config or default_sort_config(fields_map)
    statements = [rule.compile(config, context) for rule in sorting_rules]
    return statements, context


def try_parse_dict(
    sorting_rules: list[dict], *, syntax_types: list[type[AbstractSortRule]] = None
) -> list[AbstractSortRule]:
    """
    Try to parse the given sorting rules as a list of AbstractSortRule.

    :param sorting_rules: the sorting rules to parse.
    :param syntax_types: the syntax types to use to parse the sorting rules.
    :return: the list of parsed rules.
    """
    syntax_types = syntax_types or [SortRule]
    rules = []
    for sorting_rule in sorting_rules:
        for syntax_type in syntax_types:
            rule = syntax_type.try_parse_dict(sorting_rule)
            if rule:
                rules.append(rule)
    return rules
