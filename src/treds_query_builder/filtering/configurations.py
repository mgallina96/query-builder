from treds_query_builder.filtering import CompilationConfig
from treds_query_builder.filtering.models import FieldMap
from treds_query_builder.filtering.models.conditions import (
    AndCondition,
    NotCondition,
    OrCondition,
)
from treds_query_builder.filtering.models.operators import (
    AllOperator,
    AnyOperator,
    CaseInsensitiveContainsOperator,
    CaseInsensitiveEndsWithOperator,
    CaseInsensitiveEqualsOperator,
    CaseInsensitiveLikeOperator,
    CaseInsensitiveNotEqualsOperator,
    CaseInsensitiveStartsWithOperator,
    ContainsOperator,
    EndsWithOperator,
    EqualsOperator,
    GreaterThanOperator,
    GreaterThanOrEqualOperator,
    InOperator,
    IsEmptyOperator,
    IsNotEmptyOperator,
    IsNotNullOperator,
    IsNullOperator,
    LessThanOperator,
    LessThanOrEqualOperator,
    LikeOperator,
    NotEqualsOperator,
    NotInOperator,
    StartsWithOperator,
)
from treds_query_builder.filtering.models.rules import (
    ComplexFilterRule,
    SimpleFilterRule,
)

default_all_operators = [
    EqualsOperator(),
    CaseInsensitiveEqualsOperator(),
    LikeOperator(),
    CaseInsensitiveLikeOperator(),
    NotEqualsOperator(),
    CaseInsensitiveNotEqualsOperator(),
    ContainsOperator(),
    CaseInsensitiveContainsOperator(),
    InOperator(),
    NotInOperator(),
    GreaterThanOperator(),
    GreaterThanOrEqualOperator(),
    LessThanOperator(),
    LessThanOrEqualOperator(),
    IsNullOperator(),
    IsNotNullOperator(),
    IsEmptyOperator(),
    IsNotEmptyOperator(),
    StartsWithOperator(),
    CaseInsensitiveStartsWithOperator(),
    EndsWithOperator(),
    CaseInsensitiveEndsWithOperator(),
    AnyOperator(),
    AllOperator(),
]

default_all_conditions = [
    AndCondition(),
    OrCondition(),
    NotCondition(),
]


def default_filters_config(fields_mapping: list[FieldMap]) -> CompilationConfig:
    return CompilationConfig(
        fields_mapping=fields_mapping,
        conditions=default_all_conditions,
        operators=default_all_operators,
        syntax_types=[ComplexFilterRule, SimpleFilterRule],
    )
