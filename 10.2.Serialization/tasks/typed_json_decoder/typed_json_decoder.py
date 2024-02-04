import typing as tp
import json

from decimal import Decimal


def as_custom_type(dct: dict[str, tp.Any]) -> dict[tp.Any, tp.Any]:
    val = dct.get("__custom_key_type__")
    if val is not None:
        types: dict[str, type] = {
            "int": int,
            "float": float,
            "decimal": Decimal
        }
        vl = types[val]
        del dct['__custom_key_type__']
        kys = set(dct.keys())
        for i in kys:
            dct[vl(i)] = dct.pop(i)
    return dct


def decode_typed_json(json_value: str) -> tp.Any:
    """
    Returns deserialized object from json string.
    Checks __custom_key_type__ in object's keys to choose appropriate type.

    :param json_value: serialized object in json format
    :return: deserialized object
    """
    return json.loads(json_value, object_hook=as_custom_type)
