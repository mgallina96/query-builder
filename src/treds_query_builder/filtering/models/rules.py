from typing import Any

from treds_query_builder.filtering import AbstractFilterRule, CompilationConfig, CompilationContext


class SimpleFilterRule(AbstractFilterRule):
    field: str
    operator: str
    value: Any

    def __init__(self, field: str, operator: str, value: Any):
        self.field = field
        self.operator = operator
        self.value = value

    def compile(self, config: CompilationConfig, context: CompilationContext):
        field_map = config.get_field(self.field)
        return config.get_operator(self.operator).apply(
            config, context, field_map, field_map.transform(self.value)
        )

    @staticmethod
    def try_parse_dict(dictionary: dict) -> "SimpleFilterRule":
        if "field" in dictionary and "operator" in dictionary and "value" in dictionary:
            return SimpleFilterRule(
                dictionary["field"], dictionary["operator"], dictionary["value"]
            )


class ComplexFilterRule(AbstractFilterRule):
    condition: str
    rules: list[AbstractFilterRule]

    def __init__(self, condition: str, rules: list[AbstractFilterRule]):
        self.condition = condition
        self.rules = rules

    def compile(self, config: CompilationConfig, context: CompilationContext):
        compiled_rules = [rule.compile(config, context) for rule in self.rules if rule]
        return config.get_condition(self.condition).join(compiled_rules)

    @staticmethod
    def try_parse_dict(dictionary: dict) -> "ComplexFilterRule":
        if "condition" in dictionary and "rules" in dictionary:
            return ComplexFilterRule(
                dictionary["condition"],
                [
                    ComplexFilterRule.try_parse_dict(rule_dict)
                    or SimpleFilterRule.try_parse_dict(rule_dict)
                    for rule_dict in dictionary["rules"]
                ],
            )
