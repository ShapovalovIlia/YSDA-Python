import typing as tp


def traverse_dictionary_immutable(
        dct: tp.Mapping[str, tp.Any],
        prefix: str = "") -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    visited = set()
    lst: list[tuple[str, int]] = []
    for key, value in dct.items():
        current_key = prefix + "." + key if prefix else key
        if current_key not in visited:
            visited.add(current_key)
            if isinstance(value, dict):
                lst.extend(traverse_dictionary_immutable(value, current_key))
            else:
                lst.append((current_key, value))
    return lst


def traverse_dictionary_mutable(
        dct: tp.Mapping[str, tp.Any],
        result: list[tuple[str, int]],
        prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    visited = set()
    for key, value in dct.items():
        current_key = prefix + "." + key if prefix else key
        if current_key not in visited:
            visited.add(current_key)
            if isinstance(value, dict):
                (traverse_dictionary_mutable(value, result, current_key))
            else:
                result.append((current_key, value))


def traverse_dictionary_iterative(
        dct: tp.Mapping[str, tp.Any]
) -> list[tuple[str, int]]:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """

    result: list[tuple[str, int]] = []
    stack: list[tuple[tuple[str, ...], tp.Mapping[str, tp.Any]]] = [((), dct)]

    while stack:
        path, current_dict = stack.pop()

        for key, value in current_dict.items():
            current_key = path + (key,)
            if isinstance(value, dict):
                stack.append((current_key, value))
            else:
                full_key = ".".join(current_key)
                result.append((full_key, value))

    return result
