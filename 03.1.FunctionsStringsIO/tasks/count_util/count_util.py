def count_util(text: str, flags: str | None = None) -> dict[str, int]:
    """
    :param text: text to count entities
    :param flags: flags in command-like format - can be:
        * -m stands for counting characters
        * -l stands for counting lines
        * -L stands for getting length of the longest line
        * -w stands for counting words
    More than one flag can be passed at the same time, for example:
        * "-l -m"
        * "-lLw"
    Ommiting flags or passing empty string is equivalent to "-mlLw"
    :return: mapping from string keys to corresponding counter, where
    keys are selected according to the received flags:
        * "chars" - amount of characters
        * "lines" - amount of lines
        * "longest_line" - the longest line length
        * "words" - amount of words
    """
    dct: dict[str, int] = dict()

    if flags is None or flags == '' or 'm' in flags:
        dct["chars"] = len(text)

    if flags is None or flags == '' or 'l' in flags:
        dct["lines"] = text.count('\n')

    if flags is None or flags == '' or 'L' in flags:
        dct["longest_line"] = max(len(line) for line in text.split('\n'))

    if flags is None or flags == '' or 'w' in flags:
        dct["words"] = len(text.split())

    return dct
