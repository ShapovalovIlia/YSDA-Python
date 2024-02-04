import typing as tp


#
class PropertyConverterMeta(type):
    def __new__(cls, name: tp.Any, bases: tp.Any, attrs: tp.Any) -> tp.Any:
        new_attrs = {}
        getters = {}
        setters = {}

        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and attr_name.startswith("get_"):
                getters[attr_name[4:]] = attr_value
            elif callable(attr_value) and attr_name.startswith("set_"):
                setters[attr_name[4:]] = attr_value
            else:
                new_attrs[attr_name] = attr_value

        for base in bases:
            for attr_name, attr_value in base.__dict__.items():
                if callable(attr_value) and attr_name.startswith("get_"):
                    getters[attr_name[4:]] = attr_value
                elif callable(attr_value) and attr_name.startswith("set_"):
                    setters[attr_name[4:]] = attr_value
                else:
                    new_attrs[attr_name] = attr_value

        for name in getters.keys() | setters.keys():
            if name not in new_attrs:
                new_attrs[name] = property(getters.get(name), setters.get(name))

        return super().__new__(cls, name, bases, new_attrs)


class PropertyConverter(metaclass=PropertyConverterMeta):
    def __getattr__(self, attr: str) -> tp.Any:
        return object.__getattribute__(self, attr)

    def __setattr__(self, attr: str, value: tp.Any) -> None:
        object.__setattr__(self, attr, value)
