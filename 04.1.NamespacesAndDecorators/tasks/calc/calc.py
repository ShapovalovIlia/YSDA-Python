import math
from typing import Any

PROMPT = '>>> '


def run_calc(context: dict[str, Any] | None = None) -> None:
    """Run interactive calculator session in specified namespace"""
    if context is not None:
        context.update({"__builtins__": {}})
    else:
        context = {"__builtins__": {}}
    while True:
        try:
            user_input = input(PROMPT)
            result = eval(user_input, context)
            print(result)
        except EOFError:
            print()
            break
        except Exception as e:
            raise NameError(e)


if __name__ == '__main__':
    context = {'math': math}
    run_calc(context)
