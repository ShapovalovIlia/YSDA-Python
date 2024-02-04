import typing as tp


class Kelvin:
    def __init__(self, attr_name: str) -> None:
        self.attr_name = attr_name

    def __get__(self, instance: object, owner: type[object]) -> tp.Union['Kelvin', int]:
        if instance is None:
            return self
        return getattr(instance, self.attr_name)

    def __set__(self, instance: object, value: int) -> None:
        if value <= 0:
            raise ValueError("Temperature in Kelvin must be greater than 0")
        if not hasattr(instance, self.attr_name):
            raise AttributeError(f"Attribute '{self.attr_name}' not found")
        setattr(instance, self.attr_name, value)

    def __delete__(self, instance: object) -> None:
        raise ValueError("Can't delete attribute")


class Celsius:
    def __init__(self, kelvin_attr: str) -> None:
        self.kelvin_attr = kelvin_attr

    def __get__(self, instance: object, owner: type[object]) -> tp.Union['Celsius', int]:
        if instance is None:
            return self
        if not hasattr(instance, self.kelvin_attr):
            raise AttributeError(f"Attribute '{self.kelvin_attr}' not found")
        kelvin_field = getattr(owner, self.kelvin_attr, None)
        if not isinstance(kelvin_field, Kelvin):
            raise AttributeError(f"{self.kelvin_attr} must be of type Kelvin")
        kelvin_value = getattr(instance, self.kelvin_attr)
        return kelvin_value - 273

    def __set__(self, instance: object, value: int) -> None:
        raise AttributeError("Can't set value")

    def __delete__(self, instance: object) -> None:
        raise ValueError("Can't delete attribute")
