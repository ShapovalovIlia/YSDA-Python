import numpy as np
import numpy.typing as npt


def max_element(array: npt.NDArray[np.int_]) -> int | None:
    """
    Return max element before zero for input array.
    If appropriate elements are absent, then return None
    :param array: array,
    :return: max element value or None
    """
    mask = np.roll(array == 0, 1)
    mask[0] = False
    elements_after_zero = array[mask]
    return np.max(elements_after_zero) if elements_after_zero.size > 0 else None
