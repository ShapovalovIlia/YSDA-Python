import zlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class BlobType(Enum):
    """Helper class for holding blob type"""
    COMMIT = b'commit'
    TREE = b'tree'
    DATA = b'blob'

    @classmethod
    def from_bytes(cls, type_: bytes) -> 'BlobType':
        for member in cls:
            if member.value == type_:
                return member
        assert False, f'Unknown type {type_.decode("utf-8")}'


@dataclass
class Blob:
    """Any blob holder"""
    type_: BlobType
    content: bytes


@dataclass
class Commit:
    """Commit blob holder"""
    tree_hash: str
    parents: list[str]
    author: str
    committer: str
    message: str


@dataclass
class Tree:
    """Tree blob holder"""
    children: dict[str, Blob]


def read_blob(path: Path) -> Blob:
    """
    Read blob-file, decompress and parse header
    :param path: path to blob-file
    :return: blob-file type and content
    """
    with path.open('rb') as file:
        blob_type, content = zlib.decompress(file.read()).split(b'\x00', 1)
        blob_type = blob_type.split(b' ')[0]
        return Blob(type_=BlobType.from_bytes(blob_type), content=content)


def traverse_objects(obj_dir: Path) -> dict[str, Blob]:
    """
    Traverse directory with git objects and load them
    :param obj_dir: path to git "objects" directory
    :return: mapping from hash to blob with every blob found
    """
    dct: dict[str, Blob] = {}
    for dr in obj_dir.iterdir():
        for file in dr.iterdir():
            dct[dr.name + file.name] = read_blob(file)

    return dct


def parse_commit(blob: Blob) -> Commit:
    """
    Parse commit blob
    :param blob: blob with commit type
    :return: parsed commit
    """
    lines = blob.content.decode().split('\n')
    return Commit(tree_hash=next(line for line in lines if line.startswith('tree')).split()[1],
                  parents=[line.split()[1] for line in [line for line in lines if line.startswith('parent')]],
                  author=next(line for line in lines if line.startswith('author'))[7:],
                  committer=next(line for line in lines if line.startswith('committer'))[10:],
                  message='\n'.join(lines[lines.index('') + 1:]).strip())


def parse_tree(blobs: dict[str, Blob], tree_root: Blob, ignore_missing: bool = True) -> Tree:
    """
    Parse tree blob
    :param blobs: all read blobs (by traverse_objects)
    :param tree_root: tree blob to parse
    :param ignore_missing: ignore blobs which were not found in objects directory
    :return: tree contains children blobs (or only part of them found in objects directory)
    NB. Children blobs are not being parsed according to type.
        Also nested tree blobs are not being traversed.
    """
    child = {}
    content = tree_root.content

    while content:
        content = content[content.find(b' ') + 1:]
        end = content.find(b'\x00')
        name = content[:end].decode()
        content = content[end + 1:]
        child_hash = content[:20].hex()
        content = content[20:]
        if child_hash in blobs:
            child[name] = blobs[child_hash]

    return Tree(children=child)


def find_initial_commit(blobs: dict[str, Blob]) -> Commit:
    """
    Iterate over blobs and find initial commit (without parents)
    :param blobs: blobs read from objects dir
    :return: initial commit
    """
    for b in blobs.values():
        if b.type_ == BlobType.COMMIT:
            commit = parse_commit(b)
            if not commit.parents:
                return commit
    raise ValueError("Initial commit not found")


def search_file(blobs: dict[str, Blob], tree_root: Blob, filename: str) -> Blob:
    """
    Traverse tree blob (can have nested tree blobs) and find requested file,
    check if file was not found (assertion).
    :param blobs: blobs read from objects dir
    :param tree_root: root blob for traversal
    :param filename: requested file
    :return: requested file blob
    """
    for name, child_blob in parse_tree(blobs, tree_root).children.items():
        if name == filename:
            return child_blob
        if child_blob and child_blob.type_ == BlobType.TREE:
            found = search_file(blobs, child_blob, filename)
            if found:
                return found
    raise ValueError(f"File {filename} not found")
