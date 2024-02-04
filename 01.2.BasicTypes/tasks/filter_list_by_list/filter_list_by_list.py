def filter_list_by_list(lst_a: list[int] | range, lst_b: list[int] | range) -> list[int]:
    """
    Filter first sorted list by other sorted list
    :param lst_a: first sorted list
    :param lst_b: second sorted list
    :return: filtered sorted list
    """
    list = []
    n = len(lst_a)
    m = len(lst_b)
    i, j = 0, 0
    while i < n and j < m:
        if lst_a[i] < lst_b[j]:
            list.append(lst_a[i])
            i += 1
        elif lst_a[i] > lst_b[j]:
            j += 1
        else:
            i += 1
    while i < n:
        list.append(lst_a[i])
        i += 1
    return list
