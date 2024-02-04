import typing as tp
from collections import Counter


def get_min_to_drop(seq: tp.Sequence[tp.Any]) -> int:
    """
    :param seq: sequence of elements
    :return: number of elements need to drop to leave equal elements
    """
    ln = len(seq)
    dct = Counter(seq)
    m = max(dct.values()) if ln > 0 else 0
    return ln - m
