import multiprocessing
import threading
import time


def very_slow_function(x: int) -> int:
    """Function which calculates square of given number really slowly
    :param x: given number
    :return: number ** 2
    """
    time.sleep(0.3)
    return x ** 2


def calc_squares_simple(bound: int) -> list[int]:
    """Function that calculates squares of numbers in range [0; bound)
    :param bound: positive upper bound for range
    :return: list of squared numbers
    """
    return [very_slow_function(i) for i in range(bound)]


def calc_squares_multithreading(bound: int) -> list[int]:
    """Function that calculates squares of numbers in range [0; bound)
    using threading.Thread
    :param bound: positive upper bound for range
    :return: list of squared numbers
    """
    res: list[int] = [0] * bound

    def func(i: int, res: list[int]) -> None:
        res[i] = very_slow_function(i)

    threads = [
        threading.Thread(target=lambda i=i: func(i, res))
        for i in range(bound)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return res


def calc_squares_multiprocessing(bound: int) -> list[int]:
    """Function that calculates squares of numbers in range [0; bound)
    using multiprocessing.Pool
    :param bound: positive upper bound for range
    :return: list of squared numbers
    """
    with multiprocessing.Pool() as pool:
        results = pool.map(very_slow_function, range(bound))
    return results
