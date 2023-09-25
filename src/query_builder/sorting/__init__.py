from query_builder.shared.models import FieldMap
from query_builder.sorting.configurations import (
    default_sort_config,
)
from query_builder.sorting.errors import QueryBuilderSortSyntaxError
from query_builder.sorting.models import CompilationConfig, AbstractSortRule


def apply_sorting(
    sorting_rules: list[dict] | list[AbstractSortRule],
    fields_map: list[FieldMap],
    *queries,
    config: CompilationConfig = None,
) -> tuple:
    """
    Parse the sorting rules and build the SQL order by statement to append
    to the given SqlAlchemy queries.

    :param sorting_rules: The sort rules to build.
    :param fields_map: The mapping between the 'field' inside the rule and the SqlAlchemy Column.
    :param queries: The SqlAlchemy queries to process.
    :param config: The configuration to use to parse the rules.
    :return: The SqlAlchemy queries with the sort applied.
    """
    if not isinstance(sorting_rules, list):
        raise QueryBuilderSortSyntaxError("Sort rules must be a list")
    compiled_rules = build_sorting(sorting_rules, fields_map, config)
    return tuple([query.order_by(*compiled_rules) for query in queries])


def build_sorting(
    sorting_rules: list[dict] | list[AbstractSortRule],
    fields_map: list[FieldMap],
    config: CompilationConfig = None,
):
    """
    Parse the sorting rules and build the corresponding SQL order by statement.

    :param sorting_rules: the sorting rules to build.
    :param fields_map: the mapping between the 'field' inside the rule and the SqlAlchemy Column.
    :param config: the configuration to use to parse the rules.
    :return: the order by statement.
    """
    config = config or default_sort_config(fields_map)
    return [rule.compile(config) for rule in try_parse_dict(sorting_rules, config)]


def try_parse_dict(
    sorting_rules: list[dict] | list[AbstractSortRule], config: CompilationConfig
) -> list[AbstractSortRule]:
    """
    Try to parse the given sorting rules as a list of AbstractSortRule.
    :param sorting_rules: the sorting rules to parse.
    :param config: the configuration to use to parse the rules.
    :return: the list of parsed rules.
    """
    rules = []
    for sorting_rule in sorting_rules:
        if isinstance(sorting_rule, AbstractSortRule):
            rules.append(sorting_rule)
        else:
            for syntax_type in config.syntax_types:
                rule = syntax_type.try_parse_dict(sorting_rule)
                if rule:
                    rules.append(rule)
    return rules
