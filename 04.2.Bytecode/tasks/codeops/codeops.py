import types
import dis


def count_operations(source_code: types.CodeType) -> dict[str, int]:
    """Count byte code operations in given source code.

    :param source_code: the bytecode operation names to be extracted from
    :return: operation counts
    """
    d: dict[str, int] = dict()

    def recursive_count(source_code: types.CodeType) -> dict[str, int]:
        instructions = dis.get_instructions(source_code)
        for i in instructions:
            op_name = i.opname
            d[op_name] = d.get(op_name, 0) + 1
            argval = i.argval
            if isinstance(argval, types.CodeType):
                recursive_count(argval)
        return d

    return recursive_count(source_code)
