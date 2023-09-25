from enum import Enum
from typing import Any

from query_builder.shared.models import FieldMap
from query_builder.sorting.models import AbstractDirection, CompilationConfig


class Directions(Enum):
    ASC = "asc"
    DESC = "desc"


class AscDirection(AbstractDirection):
    def __init__(self, code: str = Directions.ASC.value):
        super().__init__(code)

    def apply(self, config: CompilationConfig, field_map: FieldMap) -> Any:
        return field_map.database_column


class DescDirection(AbstractDirection):
    def __init__(self, code: str = Directions.DESC.value):
        super().__init__(code)

    def apply(self, config: CompilationConfig, field_map: FieldMap) -> Any:
        return field_map.database_column.desc()
