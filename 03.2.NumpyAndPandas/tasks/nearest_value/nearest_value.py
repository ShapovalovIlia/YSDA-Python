import numpy as np
import numpy.typing as npt


def nearest_value(matrix: npt.NDArray[np.float_], value: float) -> float | None:
    """
    Find nearest value in matrix.
    If matrix is empty return None
    :param matrix: input matrix
    :param value: value to find
    :return: nearest value in matrix or None
    """
    if matrix.size == 0:
        return None

    idx = np.abs(matrix - value).argmin()

    return float(matrix[np.unravel_index(idx, matrix.shape)])
