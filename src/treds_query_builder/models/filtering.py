from abc import ABC, abstractmethod
from typing import Any

from treds_query_builder import ApiFiltersSyntaxError


class CompilationContext:
    params: dict[str, Any]
    param_counters: dict[str, int]

    def __init__(self):
        self.params = {}
        self.param_counters = {}


class FieldMap:
    name: str
    database_column: Any

    def __init__(self, name: str, database_column: Any):
        self.name = name
        self.database_column = database_column


class AbstractCondition(ABC):
    name: str

    @abstractmethod
    def join(self, compiled_rules: list):
        raise NotImplementedError()


class AbstractOperator(ABC):
    code: str

    @staticmethod
    def _add_param(context: CompilationContext, field: FieldMap, value: Any):
        param_counter = context.param_counters.get(field.name, 0)
        param_name = f"{field.name}_{param_counter}"
        context.params |= {param_name: value}
        context.param_counters |= {field.name: param_counter + 1}
        return param_name

    @abstractmethod
    def apply(self, context: CompilationContext, field: FieldMap, value: Any):
        raise NotImplementedError()


class CompilationConfig:
    fields_mapping: list[FieldMap]
    conditions: list[AbstractCondition]
    operators: list[AbstractOperator]

    def __init__(
        self,
        fields_mapping: list[FieldMap],
        conditions: list[AbstractCondition],
        operators: list[AbstractOperator],
    ):
        self.fields_mapping = fields_mapping
        self.conditions = conditions
        self.operators = operators


class AbstractFilterRule(ABC):
    @abstractmethod
    def compile(self, config: CompilationConfig, context: CompilationContext):
        raise NotImplementedError()


class SimpleFilterRule(AbstractFilterRule):
    field: str
    operator: str
    value: Any

    def __init__(self, field: str, operator: str, value: Any):
        self.field = field
        self.operator = operator
        self.value = value

    def compile(self, config: CompilationConfig, context: CompilationContext):
        field_map = None
        for field in config.fields_mapping:
            if field.name.casefold() == self.field.casefold():
                field_map = field
                break
        if field_map is None:
            raise ApiFiltersSyntaxError(f"Invalid field '{self.field}'")

        operator = None
        for op in config.operators:
            if op.code.casefold() == self.operator.casefold():
                operator = op
                break
        if operator is None:
            raise ApiFiltersSyntaxError(f"Invalid operator '{self.operator}'")

        return operator.apply(context, field_map, self.value)


class ComplexFilterRule(AbstractFilterRule):
    condition: str
    rules: list[AbstractFilterRule]

    def __init__(self, condition: str, rules: list[AbstractFilterRule]):
        self.condition = condition
        self.rules = rules

    def compile(self, config: CompilationConfig, context: CompilationContext):
        compiled_rules = []
        for rule in self.rules:
            compiled_rules.append(rule.compile(config, context))
        if len(compiled_rules) == 0:
            raise ApiFiltersSyntaxError("At least one rule is required")
        for condition in config.conditions:
            if condition.name.casefold() == self.condition.casefold():
                return condition.join(compiled_rules)
        raise ApiFiltersSyntaxError(f"Invalid condition '{self.condition}'")
