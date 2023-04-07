from typing import Any

from sqlalchemy import bindparam, func

from treds_query_builder.models.filtering import (
    FieldMap,
    AbstractOperator,
    CompilationContext,
)


class EqualsOperator(AbstractOperator):
    def __init__(self, code: str = "equal"):
        self.code = code

    def apply(self, context: CompilationContext, field: FieldMap, value: Any):
        return field.database_column == bindparam(
            self._add_param(context, field, value)
        )


class CaseInsensitiveEqualsOperator(AbstractOperator):
    def __init__(self, code: str = "iequal"):
        self.code = code

    def apply(self, context: CompilationContext, field: FieldMap, value: Any):
        return func.lower(field.database_column) == func.lower(
            bindparam(self._add_param(context, field, value))
        )


class LikeOperator(AbstractOperator):
    def __init__(self, code: str = "like"):
        self.code = code

    def apply(self, context: CompilationContext, field: FieldMap, value: Any):
        return field.database_column.like(
            bindparam(self._add_param(context, field, value))
        )


class CaseInsensitiveLikeOperator(AbstractOperator):
    def __init__(self, code: str = "ilike"):
        self.code = code

    def apply(self, context: CompilationContext, field: FieldMap, value: Any):
        return field.database_column.ilike(
            bindparam(self._add_param(context, field, value))
        )


class NotEqualsOperator(AbstractOperator):
    def __init__(self, code: str = "notequal"):
        self.code = code

    def apply(self, context: CompilationContext, field: FieldMap, value: Any):
        return field.database_column != bindparam(
            self._add_param(context, field, value)
        )


class CaseInsensitiveNotEqualsOperator(AbstractOperator):
    def __init__(self, code: str = "inotequal"):
        self.code = code

    def apply(self, context: CompilationContext, field: FieldMap, value: Any):
        return func.lower(field.database_column) != func.lower(
            bindparam(self._add_param(context, field, value))
        )


class ContainsOperator(AbstractOperator):
    def __init__(self, code: str = "contains"):
        self.code = code

    def apply(self, context: CompilationContext, field: FieldMap, value: Any):
        return field.database_column.like(
            bindparam(self._add_param(context, field, f"%{value}%"))
        )


class CaseInsensitiveContainsOperator(AbstractOperator):
    def __init__(self, code: str = "icontains"):
        self.code = code

    def apply(self, context: CompilationContext, field: FieldMap, value: Any):
        return field.database_column.ilike(
            bindparam(self._add_param(context, field, f"%{value}%"))
        )
