from sqlalchemy import select, text

from treds_query_builder.filtering import apply_filters
from treds_query_builder.filtering.configurations import default_filters_config
from treds_query_builder.filtering.models import FieldMap

if __name__ == "__main__":
    config = default_filters_config(
        [
            FieldMap("id", text("TestEntity.id")),
            FieldMap("username", text("TestEntity.username")),
        ]
    )
    query = select(text("* from TestEntity"))
    (query,) = apply_filters(
        {
            "condition": "and",
            "rules": [
                {"field": "id", "operator": "equal", "value": 1},
                {"field": "username", "operator": "equal", "value": "test"},
            ],
        },
        config,
        query,
    )

    print(str(query))
