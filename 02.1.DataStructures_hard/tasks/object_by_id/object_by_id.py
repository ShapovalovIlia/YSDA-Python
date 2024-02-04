import ctypes
import struct
import typing as tp

LONG_LEN = 8
INT_LEN = 4
CHAR_LEN = 1

ULONG_CHAR = "L" if ctypes.sizeof(ctypes.c_ulong) == 8 else "Q"
LONG_CHAR = "l" if ctypes.sizeof(ctypes.c_long) == 8 else "q"
INT_CHAR = "i"


def obtain_int_by_id(obj_id: int, existing_data: dict[int, tp.Any]) -> None:
    segments = struct.unpack(LONG_CHAR, ctypes.string_at(obj_id + 2 * LONG_LEN, LONG_LEN))[0]
    is_neg = False
    if segments < 0:
        segments = -segments
        is_neg = True
    value = 0
    factor = 1
    for i in range(0, segments):
        piece = struct.unpack(INT_CHAR, ctypes.string_at(obj_id + (3 * LONG_LEN) + (i * INT_LEN), INT_LEN))[0]
        value += piece * factor
        factor *= 2 ** 30
    if is_neg:
        value = -value
    existing_data[obj_id] = value


def obtain_bool_by_id(obj_id: int, existing_data: dict[int, tp.Any]) -> None:
    existing_data[obj_id] = bool(struct.unpack(INT_CHAR, ctypes.string_at(obj_id + 3 * LONG_LEN, INT_LEN))[0])


def obtain_float_by_id(obj_id: int, existing_data: dict[int, tp.Any]) -> None:
    existing_data[obj_id] = struct.unpack("d", ctypes.string_at(obj_id + 2 * LONG_LEN, LONG_LEN))[0]


def obtain_str_by_id(obj_id: int, existing_data: dict[int, tp.Any]) -> None:
    existing_data[obj_id] = \
        struct.unpack(str(struct.unpack(ULONG_CHAR, ctypes.string_at(obj_id + 2 * LONG_LEN, LONG_LEN))[0]) + "s",
                      ctypes.string_at(obj_id + (4 * LONG_LEN) + 16,
                                       struct.unpack(ULONG_CHAR, ctypes.string_at(obj_id + 2 * LONG_LEN, LONG_LEN))[
                                           0]))[
            0].decode("ascii")


def obtain_list_by_id(obj_id: int, existing_data: dict[int, tp.Any]) -> None:
    existing_data[obj_id] = []
    for reference in struct.unpack(
            str(struct.unpack(ULONG_CHAR, ctypes.string_at(obj_id + 2 * LONG_LEN, LONG_LEN))[0]) + ULONG_CHAR,
            ctypes.string_at(struct.unpack(ULONG_CHAR, ctypes.string_at(obj_id + 3 * LONG_LEN, LONG_LEN))[0],
                             struct.unpack(ULONG_CHAR, ctypes.string_at(obj_id + 2 * LONG_LEN, LONG_LEN))[
                                 0] * LONG_LEN)):
        get(reference, existing_data)
        existing_data[obj_id].append(existing_data[reference])


def obtain_tuple_by_id(obj_id: int, existing_data: dict[int, tp.Any]) -> None:
    existing_data[obj_id] = []
    for reference in struct.unpack(
            str(struct.unpack(ULONG_CHAR, ctypes.string_at(obj_id + 2 * LONG_LEN, LONG_LEN))[0]) + ULONG_CHAR,
            ctypes.string_at(obj_id + 3 * LONG_LEN,
                             struct.unpack(ULONG_CHAR, ctypes.string_at(obj_id + 2 * LONG_LEN, LONG_LEN))[
                                 0] * LONG_LEN)):
        get(reference, existing_data)
        existing_data[obj_id].append(existing_data[reference])
    existing_data[obj_id] = tuple(existing_data[obj_id])


def get(obj_id: int, existing_data: dict[int, tp.Any]) -> None:
    if obj_id in existing_data:
        return existing_data[obj_id]

    type_id = struct.unpack(ULONG_CHAR, ctypes.string_at(obj_id + LONG_LEN, LONG_LEN))[0]
    type_funcs = {
        id(int): obtain_int_by_id,
        id(bool): obtain_bool_by_id,
        id(float): obtain_float_by_id,
        id(str): obtain_str_by_id,
        id(list): obtain_list_by_id,
        id(tuple): obtain_tuple_by_id
    }

    func = type_funcs.get(type_id)
    if func:
        func(obj_id, existing_data)


def get_object_by_id(object_id: int) -> int | float | tuple[tp.Any, ...] | list[tp.Any] | str | bool:
    """
    Restores object by id.
    :param object_id: Object Id.
    :return: An object that corresponds to object_id.
    """
    used_objects: dict[int, tp.Any] = {}
    get(object_id, used_objects)
    return used_objects[object_id]
