from abc import ABC, abstractmethod
from typing import Any

from query_builder.filtering.errors import QueryBuilderFiltersSyntaxError
from query_builder.shared.models import FieldMap


class CompilationContext:
    params: dict[str, Any]
    param_counters: dict[str, int]
    included_fields: set[str]

    def __init__(self):
        self.params = {}
        self.param_counters = {}
        self.included_fields = set()


class CompilationConfig:
    syntax_types: list[type["AbstractFilterRule"]]

    _fields_mapping: dict[str, FieldMap]
    _operators_map: dict[str, "AbstractOperator"]
    _conditions_map: dict[str, "AbstractCondition"]

    def __init__(
        self,
        fields_mapping: list[FieldMap],
        conditions: list["AbstractCondition"],
        operators: list["AbstractOperator"],
        syntax_types: list[type["AbstractFilterRule"]],
    ):
        self._fields_mapping = {field.name: field for field in fields_mapping}
        self._operators_map = {operator.code: operator for operator in operators}
        self._conditions_map = {condition.name: condition for condition in conditions}
        self.syntax_types = syntax_types

    def get_operator(self, code: str) -> "AbstractOperator":
        try:
            return self._operators_map[code]
        except KeyError:
            raise QueryBuilderFiltersSyntaxError(f"Unknown operator: {code}")

    def get_condition(self, name: str) -> "AbstractCondition":
        try:
            return self._conditions_map[name]
        except KeyError:
            raise QueryBuilderFiltersSyntaxError(f"Unknown condition: {name}")

    def get_field(self, name: str) -> FieldMap:
        try:
            return self._fields_mapping[name]
        except KeyError:
            raise QueryBuilderFiltersSyntaxError(f"Unknown field: {name}")


class AbstractFilterRule(ABC):
    @abstractmethod
    def compile(self, config: CompilationConfig, context: CompilationContext):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def try_parse_dict(dictionary: dict) -> "AbstractFilterRule":
        raise NotImplementedError()


class AbstractCondition(ABC):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def join(self, compiled_rules: list):
        raise NotImplementedError()


class AbstractOperator(ABC):
    code: str

    def __init__(self, code: str):
        self.code = code

    @staticmethod
    def _add_param(context: CompilationContext, field: FieldMap, value: Any):
        param_counter = context.param_counters.get(field.name, 0)
        param_name = f"{field.name}_{param_counter}"
        context.params |= {param_name: value}
        context.param_counters |= {field.name: param_counter + 1}
        return param_name

    @abstractmethod
    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        raise NotImplementedError()
