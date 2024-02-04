def problem01() -> dict[int, str]:
    return {7: "тип у a должен быть int | None",
            5: "Из-за tp.Optional a может быть None и плюс не определен"}


def problem02() -> dict[int, str]:
    return {5: "Операция + не определена для типа object"}


def problem03() -> dict[int, str]:
    return {9: "Подаем на вход tp.Set[float] вместо tp.Set[int]",
            13: "Подаем на вход tp.Set[bool] вместо tp.Set[int]"}


def problem04() -> dict[int, str]:
    return {9: "Мы не сможем создать методы для инта используя флоты"}


def problem05() -> dict[int, str]:
    return {11: "foo должна возвращать тип A, нельзя оверрайдя в наследниках"
                " функции менять у них возвращаемое значение"}


def problem06() -> dict[int, str]:
    return {15: "Может быть ситуация когда в T нету метода, который есть в S"
                "поэтому несовместимые типы"}


def problem07() -> dict[int, str]:
    return {25: "Мы не можем расширить возвращаемое значение от B до A",
            27: "Мы не можем расширить возвращаемое значение от B до A "
                "и не можем сузить область аргумента от A до B",
            28: "Мы не можем сузить область аргумента от A до B"}


def problem08() -> dict[int, str]:
    return {6: "Не обязательно есть __len__",
            18: "Нету метода __iter__",
            24: "Передаем Iterator[str], а хотим Iterator[int]"}


def problem09() -> dict[int, str]:
    return {34: "У листа нет метода foo",
            37: "У C нету __len__",
            38: "f принимает Fooable, а получает callable[[int], None]",
            32: "У Fooable нету __contains__"}


def problem10() -> dict[int, str]:
    return {18: "Не сконвертить str в float",
            29: "Нужен int а не float, в дженерике указан именно инт"}
