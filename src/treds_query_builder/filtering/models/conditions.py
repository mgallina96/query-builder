from sqlalchemy import and_, not_, or_

from treds_query_builder.filtering.errors import ApiFiltersSyntaxError
from treds_query_builder.filtering.models import AbstractCondition


class AndCondition(AbstractCondition):
    def __init__(self, name: str = "and"):
        super().__init__(name)

    def join(self, compiled_rules: list):
        if len(compiled_rules) == 0:
            raise ApiFiltersSyntaxError("'and' condition requires at least one rule")
        return and_(*compiled_rules)


class OrCondition(AbstractCondition):
    def __init__(self, name: str = "or"):
        super().__init__(name)

    def join(self, compiled_rules: list):
        if len(compiled_rules) == 0:
            raise ApiFiltersSyntaxError("'or' condition requires at least one rule")
        return or_(*compiled_rules)


class NotCondition(AbstractCondition):
    def __init__(self, name: str = "not"):
        super().__init__(name)

    def join(self, compiled_rules: list):
        if len(compiled_rules) > 1:
            raise ApiFiltersSyntaxError("'not' condition can only have one rule")
        return not_(compiled_rules[0])
