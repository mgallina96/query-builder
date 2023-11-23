from abc import abstractmethod, ABC
from typing import Any

from query_builder.shared.models import FieldMap, CompilationContext
from query_builder.sorting.errors import QueryBuilderSortSyntaxError


class CompilationConfig:
    syntax_types: list[type["AbstractSortRule"]]

    _fields_mapping: dict[str, FieldMap]
    _directions_map: dict[str, "AbstractDirection"]

    def __init__(
        self,
        fields_mapping: list[FieldMap],
        directions: list["AbstractDirection"],
        syntax_types: list[type["AbstractSortRule"]],
    ):
        self._fields_mapping = {field.name: field for field in fields_mapping}
        self._directions_map = {direction.code: direction for direction in directions}
        self.syntax_types = syntax_types

    def get_direction(self, code: str) -> "AbstractDirection":
        try:
            return self._directions_map[code]
        except KeyError:
            raise QueryBuilderSortSyntaxError(f"Unknown direction: {code}")

    def get_field(self, name: str) -> FieldMap:
        try:
            return self._fields_mapping[name]
        except KeyError:
            raise QueryBuilderSortSyntaxError(f"Unknown field: {name}")


class AbstractSortRule(ABC):
    @abstractmethod
    def compile(self, config: CompilationConfig, context: CompilationContext):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def try_parse_dict(dictionary: dict) -> "AbstractSortRule":
        raise NotImplementedError()


class AbstractDirection(ABC):
    code: str

    def __init__(self, code: str):
        self.code = code

    @abstractmethod
    def apply(
        self,
        config: CompilationConfig,
        field_map: FieldMap,
    ) -> Any:
        raise NotImplementedError()
