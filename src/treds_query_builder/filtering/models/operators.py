from typing import Any

from sqlalchemy import bindparam, func, not_, text

from treds_query_builder.filtering.models import (
    AbstractOperator,
    CompilationConfig,
    CompilationContext,
    FieldMap,
)


class EqualsOperator(AbstractOperator):
    def __init__(self, code: str = "equal"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column == bindparam(
            self._add_param(context, field, value)
        )


class CaseInsensitiveEqualsOperator(AbstractOperator):
    def __init__(self, code: str = "iequal"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return func.lower(field.database_column) == func.lower(
            bindparam(self._add_param(context, field, value))
        )


class LikeOperator(AbstractOperator):
    def __init__(self, code: str = "like"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.like(
            bindparam(self._add_param(context, field, value))
        )


class CaseInsensitiveLikeOperator(AbstractOperator):
    def __init__(self, code: str = "ilike"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.ilike(
            bindparam(self._add_param(context, field, value))
        )


class NotEqualsOperator(AbstractOperator):
    def __init__(self, code: str = "notequal"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column != bindparam(
            self._add_param(context, field, value)
        )


class CaseInsensitiveNotEqualsOperator(AbstractOperator):
    def __init__(self, code: str = "inotequal"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return func.lower(field.database_column) != func.lower(
            bindparam(self._add_param(context, field, value))
        )


class ContainsOperator(AbstractOperator):
    def __init__(self, code: str = "contains"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.like(
            bindparam(self._add_param(context, field, f"%{value}%"))
        )


class CaseInsensitiveContainsOperator(AbstractOperator):
    def __init__(self, code: str = "icontains"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.ilike(
            bindparam(self._add_param(context, field, f"%{value}%"))
        )


class InOperator(AbstractOperator):
    def __init__(self, code: str = "in"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.in_(tuple(value))


class NotInOperator(AbstractOperator):
    def __init__(self, code: str = "notin"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return not_(field.database_column.in_(tuple(value)))


class GreaterThanOperator(AbstractOperator):
    def __init__(self, code: str = "greaterthan"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column > bindparam(self._add_param(context, field, value))


class GreaterThanOrEqualOperator(AbstractOperator):
    def __init__(self, code: str = "greaterthanorequal"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column >= bindparam(
            self._add_param(context, field, value)
        )


class LessThanOperator(AbstractOperator):
    def __init__(self, code: str = "lessthan"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column < bindparam(self._add_param(context, field, value))


class LessThanOrEqualOperator(AbstractOperator):
    def __init__(self, code: str = "lessthanorequal"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column <= bindparam(
            self._add_param(context, field, value)
        )


class IsNullOperator(AbstractOperator):
    def __init__(self, code: str = "isnull"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.is_(None)


class IsNotNullOperator(AbstractOperator):
    def __init__(self, code: str = "isnotnull"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.is_not(None)


class IsEmptyOperator(AbstractOperator):
    def __init__(self, code: str = "isempty"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return func.trim(field.database_column) == ""


class IsNotEmptyOperator(AbstractOperator):
    def __init__(self, code: str = "isnotempty"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return func.trim(field.database_column) != ""


class StartsWithOperator(AbstractOperator):
    def __init__(self, code: str = "startswith"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.like(
            bindparam(self._add_param(context, field, f"{value}%"))
        )


class CaseInsensitiveStartsWithOperator(AbstractOperator):
    def __init__(self, code: str = "istartswith"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.ilike(
            bindparam(self._add_param(context, field, f"{value}%"))
        )


class EndsWithOperator(AbstractOperator):
    def __init__(self, code: str = "endswith"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.like(
            bindparam(self._add_param(context, field, f"%{value}"))
        )


class CaseInsensitiveEndsWithOperator(AbstractOperator):
    def __init__(self, code: str = "iendswith"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        return field.database_column.ilike(
            bindparam(self._add_param(context, field, f"%{value}"))
        )


class AnyOperator(AbstractOperator):
    def __init__(self, code: str = "any"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        if value is not None:
            return field.database_column.any(value.compile(config, context))
        else:
            return field.database_column.any(text("1 = 1"))


class AllOperator(AbstractOperator):
    def __init__(self, code: str = "all"):
        super().__init__(code)

    def apply(
        self,
        config: CompilationConfig,
        context: CompilationContext,
        field: FieldMap,
        value: Any,
    ):
        if value is not None:
            return not_(field.database_column.any(not_(value.compile(config, context))))
        else:
            return not_(field.database_column.any(not_(text("1 = 1"))))
