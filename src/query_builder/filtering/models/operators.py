from enum import Enum
from typing import Any

from sqlalchemy import bindparam, func, not_, text

from query_builder.filtering.models import (
    AbstractOperator,
    CompilationConfig,
)
from query_builder.shared.models import FieldMap, CompilationContext


class Operators(Enum):
    EQUAL = "equal"
    IEQUAL = "iequal"
    LIKE = "like"
    ILIKE = "ilike"
    NOTEQUAL = "notequal"
    INOTEQUAL = "inotequal"
    CONTAINS = "contains"
    ICONTAINS = "icontains"
    IN = "in"
    NOTIN = "notin"
    GREATERTHAN = "greaterthan"
    GREATERTHANOREQUAL = "greaterthanorequal"
    LESSTHAN = "lessthan"
    LESSTHANOREQUAL = "lessthanorequal"
    ISNULL = "isnull"
    ISNOTNULL = "isnotnull"
    ISEMPTY = "isempty"
    ISNOTEMPTY = "isnotempty"
    STARTSWITH = "startswith"
    ISTARTSWITH = "istartswith"
    ENDSWITH = "endswith"
    IENDSWITH = "iendswith"
    ANY = "any"
    ALL = "all"


class EqualsOperator(AbstractOperator):
    def __init__(self, code: str = Operators.EQUAL.value):
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
    def __init__(self, code: str = Operators.IEQUAL.value):
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
    def __init__(self, code: str = Operators.LIKE.value):
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
    def __init__(self, code: str = Operators.ILIKE.value):
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
    def __init__(self, code: str = Operators.NOTEQUAL.value):
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
    def __init__(self, code: str = Operators.INOTEQUAL.value):
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
    def __init__(self, code: str = Operators.CONTAINS.value):
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
    def __init__(self, code: str = Operators.ICONTAINS.value):
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
    def __init__(self, code: str = Operators.IN.value):
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
    def __init__(self, code: str = Operators.NOTIN.value):
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
    def __init__(self, code: str = Operators.GREATERTHAN.value):
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
    def __init__(self, code: str = Operators.GREATERTHANOREQUAL.value):
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
    def __init__(self, code: str = Operators.LESSTHAN.value):
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
    def __init__(self, code: str = Operators.LESSTHANOREQUAL.value):
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
    def __init__(self, code: str = Operators.ISNULL.value):
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
    def __init__(self, code: str = Operators.ISNOTNULL.value):
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
    def __init__(self, code: str = Operators.ISEMPTY.value):
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
    def __init__(self, code: str = Operators.ISNOTEMPTY.value):
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
    def __init__(self, code: str = Operators.STARTSWITH.value):
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
    def __init__(self, code: str = Operators.ISTARTSWITH.value):
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
    def __init__(self, code: str = Operators.ENDSWITH.value):
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
    def __init__(self, code: str = Operators.IENDSWITH.value):
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
    def __init__(self, code: str = Operators.ANY.value):
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
    def __init__(self, code: str = Operators.ALL.value):
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
