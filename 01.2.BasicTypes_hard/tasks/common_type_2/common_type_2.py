import typing as tp


def convert_to_common_type(data: list[tp.Any]) -> list[tp.Any]:
    """
    Takes list of multiple types' elements and convert each element to common type according to given rules
    :param data: list of multiple types' elements
    :return: list with elements converted to common type
    """
    types: list[type] = [str, int, bool, float, list]
    mx = 0
    for e in data:
        if isinstance(e, tuple):
            mx = 4
            break
        if (e is not None):
            mx = max(mx, types.index(type(e)))
    tp = types[mx]


    lst = []
    for e in data:
        if e is None or e == "":
            lst.append(tp())
            continue
        if tp != str and isinstance(e, str):
            lst.append(e.split(" "))
            continue
        # if tp == int or tp == float:
        #     if not isinstance(e, bool):
        #         e = str(e)
        if isinstance(e, tuple):
            tmp = []
            for x in e:
                tmp.append(x)
            lst.append(tmp)
            continue
        if tp == list:
            if isinstance(e, list):
                lst.append(e)
                continue
            tmp = [e]
            lst.append(tmp)
            continue
        lst.append(tp(e))
    return lst
