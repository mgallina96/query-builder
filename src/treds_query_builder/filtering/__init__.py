import json
from typing import Callable

from treds_query_builder.filtering.configurations import from_legacy_params
from treds_query_builder.filtering.models import (
    AbstractFilterRule,
    CompilationConfig,
    CompilationContext,
)


def apply_filters(
    filters: dict | None,
    fields_map: dict,
    *queries,
    transformations: dict[str, Callable] = None,
    config: CompilationConfig = None,
) -> tuple:
    def try_parse_dict() -> AbstractFilterRule:
        for syntax_type in config.syntax_types:
            rule = syntax_type.try_parse_dict(filters)
            if rule:
                return rule

    if not filters:
        return tuple(queries)
    config = config or from_legacy_params(fields_map, transformations)
    context = CompilationContext()
    statement = try_parse_dict().compile(config, context)
    return tuple([query.where(statement).params(context.params) for query in queries])


def join_filters(*filters: str | dict, condition: str = "and") -> dict:
    return {
        "condition": condition,
        "rules": [json.loads(f) if isinstance(f, str) else f for f in filters if f],
    }


def string_join_filters(*filters: str | dict, condition: str = "and") -> str:
    return json.dumps(join_filters(*filters, condition=condition))
