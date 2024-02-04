import typing as tp
import heapq


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    ans = []
    heap = []

    for i, lst in enumerate(seq):
        if lst:
            heap.append((lst[0], i, 0))

    while heap:
        val, list_idx, element_idx = heapq.heappop(heap)
        ans.append(val)

        if element_idx + 1 < len(seq[list_idx]):
            next_val = seq[list_idx][element_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, element_idx + 1))

    return ans
