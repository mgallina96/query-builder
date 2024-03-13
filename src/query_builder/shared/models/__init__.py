from typing import Any, Callable


class FieldMap:
    name: str
    database_column: Any
    blocked_operators: set[str]

    _transform_function: Callable

    def __init__(
        self,
        name: str,
        database_column: Any,
        transform_function: Callable = None,
        blocked_operators: set[str] = None,
    ):
        self.name = name
        self.database_column = database_column
        self._transform_function = transform_function or (lambda x: x)
        self.blocked_operators = blocked_operators or set()

    def transform(self, value: Any) -> Any:
        if isinstance(value, list):
            return [self._transform_function(v) for v in value]
        return self._transform_function(value)


class CompilationContext:
    params: dict[str, Any]
    param_counters: dict[str, int]
    included_fields: set[str]

    def __init__(self):
        self.params = {}
        self.param_counters = {}
        self.included_fields = set()
