import numpy as np
import numpy.typing as npt


def vander(array: npt.NDArray[np.float_ | np.int_]) -> npt.NDArray[np.float_]:
    """
    Create a Vandermod matrix from the given vector.
    :param array: input array,
    :return: vandermonde matrix
    """
    return np.array(
        list(zip(*np.tile(array, (array.shape[0], 1)) ** np.arange(array.shape[0]).reshape(array.shape[0], 1))))
