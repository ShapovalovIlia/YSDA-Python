from functools import wraps
from datetime import datetime


def profiler(func):  # type: ignore
    """
    Returns profiling decorator, which counts calls of function
    and measure last function execution time.
    Results are stored as function attributes: `calls`, `last_time_taken`
    :param func: function to decorate
    :return: decorator, which wraps any function passed
    """

    @wraps(func)
    def wrapper(*args, **kwargs):  # type: ignore
        if wrapper.depth == 0:
            wrapper.calls = 1
        else:
            wrapper.calls += 1

        start_time = datetime.now()
        wrapper.depth += 1
        result = func(*args, **kwargs)
        wrapper.depth -= 1
        end_time = datetime.now()
        wrapper.last_time_taken = (end_time - start_time).total_seconds()

        return result

    wrapper.calls = 0
    wrapper.depth = 0

    return wrapper
