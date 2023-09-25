from typing import Any, Callable


class FieldMap:
    name: str
    database_column: Any

    _transform_function: Callable

    def __init__(
        self, name: str, database_column: Any, transform_function: Callable = None
    ):
        self.name = name
        self.database_column = database_column
        self._transform_function = transform_function or (lambda x: x)

    def transform(self, value: Any) -> Any:
        if isinstance(value, list):
            return [self._transform_function(v) for v in value]
        return self._transform_function(value)
