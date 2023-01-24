def normalize_query_param(value):
    """
    Given a non-flattened query parameter value,
    and if the value is a list only containing 1 item,
    then the value is flattened.

    :param value: a value from a query parameter
    :return: a normalized query parameter value
    """

    if len(value) == 1 and value[0].lower() in ["true", "false"]:

        if value[0].lower() == "true":
            return True
        return False

    return value if len(value) > 1 else value[0]


def normalize_query(params):
    """
    Converts query parameters from only containing one value for
    each parameter, to include parameters with multiple values as lists.

    :param params: a flask query parameters data structure
    :return: a dict of normalized query parameters
    """
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}


def get_query_param(key, params, default=None, many=False):
    query_params = normalize_query(params)
    selection = query_params.get(key, default)

    if isinstance(selection, list) and len(selection) > 1 and not many:
        return selection[0]

    if many and not isinstance(selection, list):
        selection = [selection]

    return selection
