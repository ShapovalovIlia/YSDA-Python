from types import FunctionType
from typing import Any

CO_VARARGS = 4
CO_VARKEYWORDS = 8

ERR_TOO_MANY_POS_ARGS = 'Too many positional arguments'
ERR_TOO_MANY_KW_ARGS = 'Too many keyword arguments'
ERR_MULT_VALUES_FOR_ARG = 'Multiple values for arguments'
ERR_MISSING_POS_ARGS = 'Missing positional arguments'
ERR_MISSING_KWONLY_ARGS = 'Missing keyword-only arguments'
ERR_POSONLY_PASSED_AS_KW = 'Positional-only argument passed as keyword argument'


def bind_args(func: FunctionType, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Bind values from `args` and `kwargs` to corresponding arguments of `func`

    :param func: function to be inspected
    :param args: positional arguments to be bound
    :param kwargs: keyword arguments to be bound
    :return: `dict[argument_name] = argument_value` if binding was successful,
             raise TypeError with one of `ERR_*` error descriptions otherwise
    """
    code = func.__code__
    d: dict[str, Any] = dict()
    names = code.co_varnames
    arg_count = code.co_argcount
    pos_only_count = code.co_posonlyargcount
    kw_only_count = code.co_kwonlyargcount
    default_values: tuple[Any, ...] = func.__defaults__ or tuple()
    local_variables = code.co_nlocals
    kw_default_values = func.__kwdefaults__
    has_varargs: bool = bool(code.co_flags & CO_VARARGS)
    has_varkw: bool = bool(code.co_flags & CO_VARKEYWORDS)
    shift = arg_count + kw_only_count - local_variables

    if has_varargs:
        vararg_name = names[shift]
        d[vararg_name] = ()
        shift += 1

    if has_varkw:
        varkw_name = names[shift]
        d[varkw_name] = {}
        shift += 1

    if len(args) > arg_count:
        if not has_varargs:
            raise TypeError(ERR_TOO_MANY_POS_ARGS)
        else:
            d[vararg_name] = args[arg_count:]

    if kw_default_values:
        for key, val in kw_default_values.items():
            if key not in names:
                raise TypeError(ERR_TOO_MANY_KW_ARGS)
            else:
                d[key] = val

    for key, val in kwargs.items():
        if key not in names:
            if not has_varkw:
                raise TypeError(ERR_TOO_MANY_KW_ARGS)
            else:
                d[varkw_name][key] = val
                continue
        if names.index(key) < pos_only_count:
            if not has_varkw:
                raise TypeError(ERR_POSONLY_PASSED_AS_KW)
            else:
                d[varkw_name][key] = val
                continue
        d[key] = val

    for i, arg_val in enumerate(args):
        if has_varargs and i >= len(args) - len(d[vararg_name]):
            break

        if names[i] in d:
            raise TypeError(ERR_MULT_VALUES_FOR_ARG)

        d[names[i]] = arg_val

    for i in range(len(args), arg_count):
        if names[i] in kwargs:
            continue

        shifted_i = i - arg_count + len(default_values)

        if shifted_i < 0 or shifted_i >= len(default_values):
            raise TypeError(ERR_MISSING_POS_ARGS)

        d[names[i]] = default_values[shifted_i]

    for i in range(pos_only_count):
        if names[i] not in d:
            raise TypeError(ERR_MISSING_POS_ARGS)

    for i in range(arg_count, arg_count + kw_only_count):
        if names[i] not in d:
            raise TypeError(ERR_MISSING_KWONLY_ARGS)

    return d
