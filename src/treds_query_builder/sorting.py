import json

from treds_query_builder import ApiSortingSyntaxError


def apply_sorting(
        sorting_rules: list[dict],
        fields_map: dict,
        *queries,
        default_sorting: list
) -> tuple:
    """
        Parse the sort rules and build the SQL order by statement to append
        to the given SqlAlchemy queries.

        :param sorting_rules: the sort rules to build.
        :param fields_map: the mapping between the 'property' inside the rule and the SqlAlchemy Column.
        :param queries: the SqlAlchemy queries to process.
        :param default_sorting: default set of sorting rules to apply.
        :return: the SqlAlchemy queries with the sort applied
        """

    if not sorting_rules or len(sorting_rules) == 0:
        sorting_rules = default_sorting
    if not isinstance(sorting_rules, list):
        raise ApiSortingSyntaxError("Sorting rules must be a list")
    compiled_rules = []
    for rule in sorting_rules:
        if "property" not in rule:
            raise ApiSortingSyntaxError(f"Missing required 'property' property")
        if rule["property"] not in fields_map:
            raise ApiSortingSyntaxError(f"Invalid field name '{rule['property']}'")
        direction = rule["direction"] if "direction" in rule else "asc"
        try:
            match direction.lower():
                case "asc" | None:
                    compiled_rules.append(fields_map[rule["property"]])
                case "desc":
                    compiled_rules.append(fields_map[rule["property"]].desc())
                case _:
                    raise ApiSortingSyntaxError(f"Invalid direction '{direction}'")
        except NotImplementedError:
            raise ApiSortingSyntaxError(f"Syntax error in rule '{json.dumps(rule)}'")
    return tuple([
        query.order_by(*compiled_rules)
        for query in queries
    ])
