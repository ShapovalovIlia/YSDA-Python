import os
import io
import os.path
import sys
import typing as tp
from pathlib import Path


def tail(filename: Path, lines_amount: int = 10, output: tp.IO[bytes] | None = None) -> None:
    """
    :param filename: file to read lines from (the file can be very large)
    :param lines_amount: number of lines to read
    :param output: stream to write requested amount of last lines from file
                   (if nothing specified stdout will be used)
    """
    chunk_sz = 2 ** 10
    chunk_ba = bytearray(chunk_sz)
    chunk_mv = memoryview(chunk_ba)
    pos = 0
    file_sz = os.path.getsize(filename)
    with open(filename, 'rb') as file:
        while lines_amount >= 0:
            pos -= chunk_sz
            if pos < -file_sz:
                chunk_sz += pos + file_sz
                pos = -file_sz
            file.seek(pos, io.SEEK_END)
            file.readinto(chunk_mv)
            for b in chunk_mv[0:chunk_sz]:
                if b == ord("\n"):
                    lines_amount -= 1
            if pos == -os.path.getsize(filename) and lines_amount >= 0:
                lines_amount = 0
                break
        for i in range(len(chunk_ba)):
            if lines_amount == 0:
                break
            pos += 1
            if chunk_ba[i] == ord("\n"):
                lines_amount += 1
        file.seek(pos, io.SEEK_END)
        if output is None:
            sys.stdout.write(file.read().decode("utf-8"))
        else:
            output.write(file.read())
