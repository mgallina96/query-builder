from typing import Any

import pytest
from sqlalchemy import text
from sqlalchemy.future import select

from query_builder.filtering import apply_filters, try_parse_dict
from query_builder.filtering.errors import QueryBuilderFiltersSyntaxError
from query_builder.filtering.models.operators import EqualsOperator
from query_builder.shared.models import FieldMap


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
@pytest.mark.parametrize(
    "filters,expected_result",
    [
        (
            {"field": "id", "operator": "greaterthanorequal", "value": 1},
            "SELECT * from TestEntity \nWHERE :id_0 <= TestEntity.id",
        ),
        (
            {"field": "id", "operator": "equal", "value": 1},
            "SELECT * from TestEntity \nWHERE :id_0 = TestEntity.id",
        ),
        (
            {
                "condition": "and",
                "rules": [
                    {"field": "id", "operator": "equal", "value": 1},
                    {"field": "username", "operator": "equal", "value": "test"},
                ],
            },
            "SELECT * from TestEntity \nWHERE :id_0 = TestEntity.id AND :username_0 = TestEntity.username",
        ),
        (
            {
                "condition": "and",
                "rules": [
                    {"field": "username", "operator": "equal", "value": "test1"},
                    {"field": "username", "operator": "equal", "value": "test2"},
                ],
            },
            "SELECT * from TestEntity \nWHERE :username_0 = TestEntity.username AND :username_1 = TestEntity.username",
        ),
    ],
)
def test_apply_filters(filters: dict[str, Any], expected_result: str):
    query = select(text("* from TestEntity"))
    (query,) = apply_filters(
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
    assert str(query) == expected_result


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def test_blocked_operator():
    with pytest.raises(QueryBuilderFiltersSyntaxError):
        apply_filters(
            try_parse_dict({"field": "id", "operator": "equal", "value": 1}),
            [
                FieldMap(
                    name="id",
                    database_column=text("TestEntity.id"),
                    blocked_operators={EqualsOperator().code},
                )
            ],
            select(text("* from TestEntity")),
        )

    (query,) = apply_filters(
        try_parse_dict({"field": "id", "operator": "greaterthanorequal", "value": 1}),
        [
            FieldMap(
                name="id",
                database_column=text("TestEntity.id"),
                blocked_operators={EqualsOperator().code},
            )
        ],
        select(text("* from TestEntity")),
    )
    assert str(query) == "SELECT * from TestEntity \nWHERE :id_0 <= TestEntity.id"
