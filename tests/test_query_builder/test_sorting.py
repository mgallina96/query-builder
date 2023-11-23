import pytest
from sqlalchemy import text
from sqlalchemy.future import select

from query_builder.shared.models import FieldMap
from query_builder.sorting import apply_sorting, try_parse_dict


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
@pytest.mark.parametrize(
    "sorting_rules,expected_result",
    [
        (
            [{"property": "username"}],
            "SELECT * from TestEntity ORDER BY TestEntity.username",
        ),
        (
            [{"property": "username", "direction": "asc"}],
            "SELECT * from TestEntity ORDER BY TestEntity.username",
        ),
        (
            [{"property": "username"}, {"property": "id", "direction": "asc"}],
            "SELECT * from TestEntity ORDER BY TestEntity.username, TestEntity.id",
        ),
        (
            [{"field": "username"}, {"field": "id", "direction": "asc"}],
            "SELECT * from TestEntity ORDER BY TestEntity.username, TestEntity.id",
        ),
    ],
)
def test_apply_sorting(sorting_rules: list[dict], expected_result: str):
    query = select(text("* from TestEntity"))
    (query,) = apply_sorting(
        try_parse_dict(sorting_rules),
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
