def get_common_type(type1: type, type2: type) -> type:
    """
    Calculate common type according to rule, that it must have the most adequate interpretation after conversion.
    Look in tests for adequacy calibration.
    :param type1: one of [bool, int, float, complex, list, range, tuple, str] types
    :param type2: one of [bool, int, float, complex, list, range, tuple, str] types
    :return: the most concrete common type, which can be used to convert both input values
    """
    primitive: list[type] = [bool, int, float, complex]
    harder: list[type] = [range, tuple, list]
    if type1 == type2 and type2 == range:
        return tuple
    if type1 in primitive and type2 in primitive:
        return primitive[max(primitive.index(type1), primitive.index(type2))]
    if type1 in harder and type2 in harder:
        return harder[max(harder.index(type1), harder.index(type2))]
    else:
        return str
