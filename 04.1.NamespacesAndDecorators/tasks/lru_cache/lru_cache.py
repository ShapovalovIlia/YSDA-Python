from collections.abc import Callable
from typing import Any, TypeVar
from functools import wraps
from collections import OrderedDict

Function = TypeVar('Function', bound=Callable[..., Any])


def cache(max_size: int) -> Callable[[Function], Function]:
    """
    Returns decorator, which stores result of function
    for `max_size` most recent function arguments.
    :param max_size: max amount of unique arguments to store values for
    :return: decorator, which wraps any function passed
    """

    def wrapper(func):  # type: ignore
        cache_dict = OrderedDict()

        @wraps(func)
        def wrapse(*args, **kwargs):  # type: ignore
            key = args
            if key in cache_dict:
                cache_dict.move_to_end(key)
                return cache_dict[key]
            result = func(*args, **kwargs)
            cache_dict[key] = result

            if len(cache_dict) > max_size:
                cache_dict.popitem(last=False)
            return result

        return wrapse

    return wrapper
