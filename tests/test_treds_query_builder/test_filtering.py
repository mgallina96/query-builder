from typing import Any

import pytest
from sqlalchemy import text
from sqlalchemy.future import select

from treds_query_builder.filtering import apply_filters


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
@pytest.mark.parametrize("filters,expected_result", [
    (
            {"field": "id", "operator": "greaterthanorequal", "value": 1},
            "SELECT * from TestEntity \nWHERE :id_0 <= TestEntity.id"
    ),
    (
            {"field": "id", "operator": "equal", "value": 1},
            "SELECT * from TestEntity \nWHERE :id_0 = TestEntity.id"
    ),
    (
            {"condition": "and", "rules": [
                {"field": "id", "operator": "equal", "value": 1},
                {"field": "username", "operator": "equal", "value": "test"}
            ]},
            "SELECT * from TestEntity \nWHERE :id_0 = TestEntity.id AND :username_0 = TestEntity.username"
    )
])
def test_apply_filters(filters: dict[str, Any], expected_result: str):
    query = select(text("* from TestEntity"))
    query, = apply_filters(filters, {
        "id": text("TestEntity.id"),
        "username": text("TestEntity.username")
    }, query)
    assert str(query) == expected_result