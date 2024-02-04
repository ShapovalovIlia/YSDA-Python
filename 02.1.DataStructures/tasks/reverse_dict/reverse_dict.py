import typing as tp


def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    dt: dict[str, list[str]] = dict()
    for k, v in dct.items():
        if v not in dt:
            dt[v] = []
        dt[v].append(k)
    return dt
