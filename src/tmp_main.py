from sqlalchemy import select, text

from treds_query_builder.models.conditions import AndCondition
from treds_query_builder.models.filtering import (
    CompilationConfig,
    CompilationContext,
    ComplexFilterRule,
    FieldMap,
    SimpleFilterRule,
)
from treds_query_builder.models.operators import EqualsOperator, LikeOperator

if __name__ == "__main__":
    configuration = CompilationConfig(
        fields_mapping=[
            FieldMap("id", text("TestEntity.id")),
            FieldMap("username", text("TestEntity.username")),
        ],
        conditions=[AndCondition()],
        operators=[EqualsOperator(), LikeOperator()],
    )

    query_builder_filter = ComplexFilterRule(
        "and",
        [
            SimpleFilterRule("id", "equal", 1),
            SimpleFilterRule("username", "equal", "test"),
        ],
    )
    compilation_context = CompilationContext()
    statement = query_builder_filter.compile(configuration, compilation_context)
    query = (
        select(text("* from TestEntity"))
        .where(statement)
        .params(compilation_context.params)
    )
    print(str(query))
