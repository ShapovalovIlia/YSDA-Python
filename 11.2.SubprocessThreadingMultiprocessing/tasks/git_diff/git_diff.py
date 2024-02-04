import subprocess
from pathlib import Path


def get_changed_dirs(git_path: Path, from_commit_hash: str, to_commit_hash: str) -> set[Path]:
    """
    Get directories which content was changed between two specified commits
    :param git_path: path to git repo directory
    :param from_commit_hash: hash of commit to do diff from
    :param to_commit_hash: hash of commit to do diff to
    :return: sequence of changed directories between specified commits
    """
    result = subprocess.run(f'git diff --name-only {from_commit_hash} {to_commit_hash}',
                            cwd=git_path, text=True, shell=True, capture_output=True)
    files = result.stdout.strip().split('\n')
    return {(git_path / Path(i).parent) for i in files}
