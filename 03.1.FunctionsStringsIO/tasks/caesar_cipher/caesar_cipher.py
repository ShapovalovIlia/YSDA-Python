import string


def caesar_encrypt(message: str, n: int) -> str:
    """Encrypt message using caesar cipher

    :param message: message to encrypt
    :param n: shift
    :return: encrypted message
    """
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    ln = len(lower)
    ans = ""
    for ch in message:
        if ch in lower:
            ans += lower[((lower.index(ch) + n) % ln)]
        elif ch in upper:
            ans += upper[((upper.index(ch) + n) % ln)]
        else:
            ans += ch
    return ans
