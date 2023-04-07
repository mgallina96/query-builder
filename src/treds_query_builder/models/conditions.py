from sqlalchemy import and_, not_, or_

from treds_query_builder import ApiFiltersSyntaxError
from treds_query_builder.models.filtering import AbstractCondition


class AndCondition(AbstractCondition):
    def __init__(self, name: str = "and"):
        self.name = name

    def join(self, compiled_rules: list):
        return and_(*compiled_rules)


class OrCondition(AbstractCondition):
    def __init__(self, name: str = "or"):
        self.name = name

    def join(self, compiled_rules: list):
        return or_(*compiled_rules)


class NotCondition(AbstractCondition):
    def __init__(self, name: str = "not"):
        self.name = name

    def join(self, compiled_rules: list):
        if len(compiled_rules) > 1:
            raise ApiFiltersSyntaxError("Not condition can only have one rule")
        return not_(compiled_rules[0])