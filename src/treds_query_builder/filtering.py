import json
from typing import Any, Callable

from sqlalchemy import bindparam, func, not_, text, and_, or_

from treds_query_builder import ApiFiltersSyntaxError


def _compile_simple_rule(
        filters: dict,
        fields_map: dict,
        params: dict,
        indexes: dict[str, int],
        transformations: dict[str, Callable]):
    transformations = transformations or {}
    if "field" not in filters:
        raise ApiFiltersSyntaxError(f"Missing required 'field' property")
    if filters["field"] not in fields_map:
        raise ApiFiltersSyntaxError(f"Invalid field name '{filters['field']}'")
    field = fields_map[filters["field"]]

    if "operator" not in filters:
        raise ApiFiltersSyntaxError(f"Missing required 'operator' property")
    operator = filters["operator"]

    value: Any | None = None
    no_value_operators = ["isnull", "isnotnull", "isempty", "isnotempty"]
    if filters["operator"] not in no_value_operators:
        if "value" not in filters:
            raise ApiFiltersSyntaxError(f"Missing required 'value' property")
        value = filters["value"]
    if value is not None:
        if filters["field"] in transformations:
            value = transformations[filters["field"]](value)

    if filters['field'] not in indexes:
        indexes |= {filters['field']: 0}
    param_name = f"{filters['field']}_{indexes[filters['field']]}"
    indexes[filters['field']] += 1

    try:
        match operator:
            case "equal":
                params |= {param_name: value}
                statement = field == bindparam(param_name)
            case "iequal":
                params |= {param_name: value}
                statement = func.lower(field) == func.lower(bindparam(param_name))
            case "like":
                params |= {param_name: value}
                statement = field.like(bindparam(param_name))
            case "ilike":
                params |= {param_name: value}
                statement = field.ilike(bindparam(param_name))
            case "notequal":
                params |= {param_name: value}
                statement = field != bindparam(param_name)
            case "inotequal":
                params |= {param_name: value}
                statement = not_(field.ilike(bindparam(param_name)))
            case "contains":
                params |= {param_name: f"%{value}%"}
                statement = field.like(bindparam(param_name))
            case "icontains":
                params |= {param_name: f"%{value}%"}
                statement = field.ilike(func.lower(bindparam(param_name)))
            case "in":
                statement = field.in_(tuple(value))
            case "notin":
                statement = not_(field.in_(tuple(value)))
            case "greaterthan":
                params |= {param_name: value}
                statement = field > bindparam(param_name)
            case "greaterthanorequal":
                params |= {param_name: value}
                statement = field >= bindparam(param_name)
            case "lessthan":
                params |= {param_name: value}
                statement = field < bindparam(param_name)
            case "lessthanorequal":
                params |= {param_name: value}
                statement = field <= bindparam(param_name)
            case "isnull":
                statement = field.is_(None)
            case "isnotnull":
                statement = field.is_not(None)
            case "isempty":
                statement = func.trim(field) == ''
            case "isnotempty":
                statement = func.trim(field) != ''
            case "any":
                if value is not None:
                    inner_statement, params = _compile_filters(value, fields_map, params, indexes, transformations)
                else:
                    inner_statement = text("1 = 1")
                statement = field.any(inner_statement)
            case "all":
                if value is not None:
                    inner_statement, params = _compile_filters(value, fields_map, params, indexes, transformations)
                else:
                    inner_statement = text("1 = 1")
                statement = not_(field.any(not_(inner_statement)))
            case _:
                raise ApiFiltersSyntaxError(f"Invalid operator '{operator}'")
    except NotImplementedError:
        raise ApiFiltersSyntaxError(f"Syntax error in rule '{json.dumps(filters)}'")
    return statement, params


def _compile_filters(
        filters: dict,
        fields_map: dict,
        params: dict,
        indexes: dict[str, int],
        transformations: dict[str, Callable]
):
    if "operator" in filters:
        return _compile_simple_rule(filters, fields_map, params, indexes, transformations)
    else:
        if "condition" not in filters:
            raise ApiFiltersSyntaxError(f"Missing required 'condition' property")
        match filters["condition"]:
            case "and":
                condition = and_
            case "or":
                condition = or_
            case "not":
                condition = not_
            case _:
                raise ApiFiltersSyntaxError(f"Invalid condition '{filters['condition']}'")
        compiled_rules = []
        if "rules" not in filters:
            raise ApiFiltersSyntaxError(f"Missing required 'rules' property")
        for rule in filters["rules"]:
            statement, params = _compile_filters(rule, fields_map, params, indexes, transformations)
            compiled_rules.append(statement)

        if filters["condition"] == "not" and len(compiled_rules) != 1:
            raise ApiFiltersSyntaxError(
                f"Invalid number of rules for 'not' condition. Expected 1, was {len(compiled_rules)}")

        return condition(*compiled_rules), params


def apply_filters(
        filters: dict[str, Any] | None,
        fields_map: dict,
        *queries,
        transformations: dict[str, Callable] = None
) -> tuple:
    """
    Parse the filter rules and build the SQL where statements to append
    to the given SqlAlchemy queries.

    :param filters: The filter rules to build.
    :param fields_map: The mapping between the 'field' inside the rule and the SqlAlchemy Column.
    :param queries: The SqlAlchemy queries to process.
    :param transformations: Functions to transform the 'value' of the rules.
    :return: The SqlAlchemy queries with the filters applied
    """
    if not filters:
        return tuple(queries)
    where_statement, query_params = _compile_filters(
        filters, fields_map, {}, {}, transformations)
    return tuple([
        query.where(where_statement).params(query_params)
        for query in queries
    ])


def join_filters(*filters: str | dict, condition: str = "and") -> dict:
    return {
        "condition": condition,
        "rules": [json.loads(f) if isinstance(f, str) else f for f in filters if f]
    }

def string_join_filters(*filters: str | dict, condition: str = "and") -> str:
    return json.dumps(join_filters(*filters, condition))

