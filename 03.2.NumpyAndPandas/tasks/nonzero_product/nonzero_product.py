import numpy as np
import numpy.typing as npt


def nonzero_product(matrix: npt.NDArray[np.int_]) -> int | None:
    """
    Compute product of nonzero diagonal elements of matrix
    If all diagonal elements are zeros, then return None
    :param matrix: array,
    :return: product value or None
    """
    dg = matrix.diagonal()
    nonzero_dg = dg[dg.nonzero()]

    if nonzero_dg.size == 0:
        return None

    return nonzero_dg.prod()
