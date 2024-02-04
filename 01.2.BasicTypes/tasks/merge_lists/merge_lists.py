def merge_iterative(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    n = len(lst_a)
    m = len(lst_b)
    i, j = 0, 0
    list_c = []
    while i < n or j < m:
        if (j == m) or (i < n and lst_a[i] < lst_b[j]):
            list_c.append(lst_a[i])
            i += 1
        else:
            list_c.append(lst_b[j])
            j += 1
    return list_c


def merge_sorted(lst_a: list[int], lst_b: list[int]) -> list[int]:
    """
    Merge two sorted lists in one sorted list using `sorted`
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: merged sorted list
    """
    list = []
    for e in lst_a:
        list.append(e)
    for e in lst_b:
        list.append(e)
    return sorted(list)
