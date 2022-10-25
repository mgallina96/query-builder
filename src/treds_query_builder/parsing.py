from typing import Any, Callable


def parse_query_id_fields(
        query: dict[str, Any],
        decode_function: Callable[[str | list[str] | None], int | list[int] | None]
) -> dict[str, Any]:
    """
    Utility to replace encoded id values in the query rules by applying a given decode function.
    Fields must use dot notation. Only fields terminating with the 'id' word are considered id fields.

    Valid id field examples: 'id', 'ID', 'user.id', 'company.user.id'

    Not valid examples: 'UserId', 'uuid', 'id.user'

    :param query: the query to process.
    :param decode_function: the function to apply.
    :return: the query with the id values replaced.
    """
    if "rules" in query:
        for i in range(len(query["rules"])):
            query["rules"].append(parse_query_id_fields(
                query["rules"].pop(0), decode_function))
    elif query["field"] and "value" in query:
        value = query["value"]
        if isinstance(query["value"], dict):
            value = parse_query_id_fields(
                query["value"], decode_function)
        else:
            tokens = query["field"].lower().split(".")
            if tokens and tokens[-1] == "id":
                value = decode_function(query["value"])
        query |= {"value": value}
    return query