from enum import Enum

from sqlalchemy import and_, not_, or_

from query_builder.filtering.errors import QueryBuilderFiltersSyntaxError
from query_builder.filtering.models import AbstractCondition


class Conditions(Enum):
    AND = "and"
    OR = "or"
    NOT = "not"


class AndCondition(AbstractCondition):
    def __init__(self, name: str = Conditions.AND.value):
        super().__init__(name)

    def join(self, compiled_rules: list):
        if len(compiled_rules) == 0:
            raise QueryBuilderFiltersSyntaxError("'and' condition requires at least one rule")
        return and_(*compiled_rules)


class OrCondition(AbstractCondition):
    def __init__(self, name: str = Conditions.OR.value):
        super().__init__(name)

    def join(self, compiled_rules: list):
        if len(compiled_rules) == 0:
            raise QueryBuilderFiltersSyntaxError("'or' condition requires at least one rule")
        return or_(*compiled_rules)


class NotCondition(AbstractCondition):
    def __init__(self, name: str = Conditions.NOT.value):
        super().__init__(name)

    def join(self, compiled_rules: list):
        if len(compiled_rules) > 1:
            raise QueryBuilderFiltersSyntaxError("'not' condition can only have one rule")
        return not_(compiled_rules[0])
