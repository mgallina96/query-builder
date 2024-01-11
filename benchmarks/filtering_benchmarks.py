import pyperf
from sqlalchemy import select, text

from query_builder.filtering import apply_filters, try_parse_dict
from query_builder.shared.models import FieldMap

filters = {
    "condition": "and",
    "rules": [
        {"field": "username", "operator": "equal", "value": "test1"},
        {"field": "username", "operator": "equal", "value": "test2"},
    ],
}


def current_method() -> None:
    query = select(text("* from TestEntity"))
    _ = apply_filters(
        try_parse_dict(filters),
        [
            FieldMap(
                name="id",
                database_column=text("TestEntity.id"),
            ),
            FieldMap(
                name="username",
                database_column=text("TestEntity.username"),
            ),
        ],
        query,
    )


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.timeit(
        name="compile filter rules",
        setup="from __main__ import current_method",
        stmt="current_method()",
    )
