from query_builder.shared.models import CompilationContext
from query_builder.sorting.models import CompilationConfig, AbstractSortRule
from query_builder.sorting.models.directions import Directions


class SortRule(AbstractSortRule):
    field: str
    direction: str

    def __init__(self, field: str, direction: str = Directions.ASC.value):
        self.field = field
        self.direction = direction

    def compile(self, config: CompilationConfig, context: CompilationContext):
        context.included_fields.add(self.field)
        field_map = config.get_field(self.field)
        return config.get_direction(self.direction).apply(config, field_map)

    @staticmethod
    def try_parse_dict(dictionary: dict) -> "SortRule":
        if "field" not in dictionary and "property" in dictionary:
            dictionary |= {"field": dictionary.pop("property")}
        if "direction" not in dictionary:
            dictionary |= {"direction": "asc"}
        if "field" in dictionary and "direction" in dictionary:
            return SortRule(dictionary["field"], str(dictionary["direction"]).lower())
