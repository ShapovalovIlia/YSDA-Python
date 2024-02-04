from typing import List, Union


def get_fizz_buzz(n: int) -> list[int | str]:
    """
    If value divided by 3 - "Fizz",
       value divided by 5 - "Buzz",
       value divided by 15 - "FizzBuzz",
    else - value.
    :param n: size of sequence
    :return: list of values.
    """
    fizz_buzz_list: List[Union[int, str]] = []

    for i in range(1, n + 1):
        add = ""
        if i % 3 == 0:
            add += "Fizz"
        if i % 5 == 0:
            add += "Buzz"
        if add == "":
            fizz_buzz_list.append(i)
        else:
            fizz_buzz_list.append(add)
    return fizz_buzz_list
