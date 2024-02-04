def get_middle_value(a: int, b: int, c: int) -> int:
    """
    Takes three values and returns middle value.
    """
    return a + b + c - max(a, b, c) - min(a, b, c)
