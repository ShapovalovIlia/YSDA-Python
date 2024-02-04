from collections.abc import Iterable, Iterator, Sized


class RangeIterator(Iterator[int]):
    """The iterator class for Range"""
    def __init__(self, range_: 'Range') -> None:
        pass

    def __iter__(self) -> 'RangeIterator':
        pass

    def __next__(self) -> int:
        pass


class Range(Sized, Iterable[int]):
    """The range-like type, which represents an immutable sequence of numbers"""

    def __init__(self, *args: int) -> None:
        """
        :param args: either it's a single `stop` argument
            or sequence of `start, stop[, step]` arguments.
        If the `step` argument is omitted, it defaults to 1.
        If the `start` argument is omitted, it defaults to 0.
        If `step` is zero, ValueError is raised.
        """

    def __iter__(self) -> 'RangeIterator':
        pass

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        pass

    def __contains__(self, key: int) -> bool:
        pass

    def __getitem__(self, key: int) -> int:
        pass

    def __len__(self) -> int:
        pass
