from query_builder.shared.models import FieldMap
from query_builder.sorting.models import CompilationConfig
from query_builder.sorting.models.directions import AscDirection, DescDirection
from query_builder.sorting.models.rules import SortRule


default_all_directions = [
    AscDirection(),
    DescDirection(),
]


def default_sort_config(fields_mapping: list[FieldMap]) -> CompilationConfig:
    return CompilationConfig(
        fields_mapping=fields_mapping,
        directions=default_all_directions,
        syntax_types=[SortRule],
    )


def from_legacy_params(fields_map: dict) -> CompilationConfig:
    fields_mapping = [
        FieldMap(
            name=field_name,
            database_column=fields_map.get(field_name),
        )
        for field_name in fields_map
    ]
    return default_sort_config(fields_mapping)
