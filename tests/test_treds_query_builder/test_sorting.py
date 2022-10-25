import pytest
from sqlalchemy import text
from sqlalchemy.future import select

from treds_query_builder.sorting import apply_sorting


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
@pytest.mark.parametrize("sorting_rules,expected_result", [
    (
            [{"property": "username"}],
            "SELECT * from TestEntity ORDER BY TestEntity.username"
    ),
    (
            [{"property": "username", "direction": "asc"}],
            "SELECT * from TestEntity ORDER BY TestEntity.username"
    ),
    (
            [{"property": "username"}, {"property": "id", "direction": "asc"}],
            "SELECT * from TestEntity ORDER BY TestEntity.username, TestEntity.id"
    ),
    (
            [],
            "SELECT * from TestEntity ORDER BY TestEntity.id"
    )
])
def test_apply_sorting(sorting_rules: list[dict], expected_result: str):
    query = select(text("* from TestEntity"))
    query, = apply_sorting(sorting_rules, {
        "id": text("TestEntity.id"),
        "username": text("TestEntity.username")
    }, query, default_sorting=[{"property": "id"}])
    assert str(query) == expected_result
