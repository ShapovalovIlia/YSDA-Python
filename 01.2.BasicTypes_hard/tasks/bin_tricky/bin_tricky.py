from collections.abc import Sequence


def find_median(nums1: Sequence[int], nums2: Sequence[int]) -> float:
    """
    Find median of two sorted sequences. At least one of sequences should be not empty.
    :param nums1: sorted sequence of integers
    :param nums2: sorted sequence of integers
    :return: middle value if sum of sequences' lengths is odd
             average of two middle values if sum of sequences' lengths is even
    """
    n = len(nums1)
    m = len(nums2)

    if n > m:
        nums1, nums2, n, m = nums2, nums1, m, n

    minn = 0
    maxx = n
    half_len = (n + m + 1) // 2

    while minn <= maxx:
        i = (minn + maxx) // 2
        j = half_len - i

        if i < n and nums2[j - 1] > nums1[i]:
            minn = i + 1
        elif i > 0 and nums1[i - 1] > nums2[j]:
            maxx = i - 1
        else:
            if i == 0:
                max_of_left = nums2[j - 1]
            elif j == 0:
                max_of_left = nums1[i - 1]
            else:
                max_of_left = max(nums1[i - 1], nums2[j - 1])

            if (n + m) % 2 == 1:
                return float(max_of_left)

            if i == n:
                min_of_right = nums2[j]
            elif j == m:
                min_of_right = nums1[i]
            else:
                min_of_right = min(nums1[i], nums2[j])

            return (max_of_left + min_of_right) / 2.0

    assert False, "Not reachable"
