from pathlib import Path
import subprocess


def python_sort(file_in: Path, file_out: Path) -> None:
    """
    Sort tsv file using python built-in sort
    :param file_in: tsv file to read from
    :param file_out: tsv file to write to
    """
    lst: list[tuple[int, str]] = []
    with open(file_in, 'r') as fin:
        for line in fin:
            prsd = list(line.split('\t'))
            lst.append((int(prsd[1]), str(prsd[0])))
    with open(file_out, 'w') as fout:
        for i in sorted(lst):
            fout.write(f'{i[1]}\t{i[0]}\n')


def util_sort(file_in: Path, file_out: Path) -> None:
    """
    Sort tsv file using sort util
    :param file_in: tsv file to read from
    :param file_out: tsv file to write to
    """
    subprocess.run(['sort', '-k2,2n', '-k1,1', str(file_in), '-o', str(file_out)])
