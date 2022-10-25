from typing import Any

import pytest

from treds_query_builder.parsing import parse_query_id_fields


@pytest.mark.parametrize("query,expected_result", [
    (
            {"field": "id", "operator": "equal", "value": "1"},
            {"field": "id", "operator": "equal", "value": 1}
    ),
    (
            {"field": "ID", "operator": "equal", "value": "1"},
            {"field": "ID", "operator": "equal", "value": 1}),
    (
            {"field": "user.id", "operator": "equal", "value": "1"},
            {"field": "user.id", "operator": "equal", "value": 1}
    ),
    (
            {"field": "company.user.id", "operator": "equal", "value": "1"},
            {"field": "company.user.id", "operator": "equal", "value": 1}
    ),
    (
            {"field": "UserId", "operator": "equal", "value": "1"},
            {"field": "UserId", "operator": "equal", "value": "1"}
    ),
    (
            {"field": "test", "operator": "equal", "value": "1"},
            {"field": "test", "operator": "equal", "value": "1"}
    ),
    (
            {"condition": "and", "rules": [
                {"field": "user.id", "operator": "equal", "value": "1"},
                {"field": "username", "operator": "equal", "value": "test"}
            ]},
            {"condition": "and", "rules": [
                {"field": "user.id", "operator": "equal", "value": 1},
                {"field": "username", "operator": "equal", "value": "test"}
            ]}
    ),
    (
            {"field": "tests", "operator": "any", "value": {
                "field": "user.id", "operator": "equal", "value": "1"
            }},
            {"field": "tests", "operator": "any", "value": {
                "field": "user.id", "operator": "equal", "value": 1
            }}
    ),
    (
            {"field": "tests", "operator": "any", "value": {
                "field": "not_user_id", "operator": "equal", "value": "1"
            }},
            {"field": "tests", "operator": "any", "value": {
                "field": "not_user_id", "operator": "equal", "value": "1"
            }}
    ),
    (
            {"field": "user.id", "operator": "any", "value": {
                "field": "not_user_id", "operator": "equal", "value": "1"
            }},
            {"field": "user.id", "operator": "any", "value": {
                "field": "not_user_id", "operator": "equal", "value": "1"
            }}
    ),
    (
            {"field": "user.id", "operator": "any", "value": {
                "field": "user.id", "operator": "equal", "value": "1"
            }},
            {"field": "user.id", "operator": "any", "value": {
                "field": "user.id", "operator": "equal", "value": 1
            }}
    )
])
def test_parse_query_id_fields(query: dict[str, Any], expected_result: dict[str, Any]):
    def mockup_decode_function(value: str | list[str] | None) -> int | list[int] | None:
        if not value:
            return None
        if isinstance(value, list):
            return [int(x) for x in value]
        return int(value)

    assert parse_query_id_fields(query, mockup_decode_function) == expected_result
