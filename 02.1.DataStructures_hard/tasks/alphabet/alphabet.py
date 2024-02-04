import enum
from collections import defaultdict


class Status(enum.Enum):
    NEW = 0
    EXTRACTED = 1
    FINISHED = 2


def extract_alphabet(
        graph: dict[str, set[str]]
) -> list[str]:
    """
    Extract alphabet from graph
    :param graph: graph with partial order
    :return: alphabet
    """
    stack = []
    order = []
    status = {c: Status.NEW for c in graph}
    in_order: defaultdict[str, bool] = defaultdict(bool)

    for start_vertex in graph:
        if status[start_vertex] is Status.FINISHED:
            continue

        stack.append(start_vertex)
        status[start_vertex] = Status.EXTRACTED

        while stack:
            current = stack[-1]

            if status[current] is Status.FINISHED:
                if not in_order[current]:
                    in_order[current] = True
                    order.append(current)
                stack.pop()
            else:
                status[current] = Status.FINISHED
                for neighbor in graph[current]:
                    if status[neighbor] is not Status.FINISHED:
                        stack.append(neighbor)
                        status[neighbor] = Status.EXTRACTED

    order.reverse()
    return order


def build_graph(
        words: list[str]
) -> dict[str, set[str]]:
    """
    Build graph from ordered words. Graph should contain all letters from words
    :param words: ordered words
    :return: graph
    """
    graph: dict[str, set[str]] = {c: set() for word in words for c in word}
    for prev_word, next_word in zip(words, words[1:]):
        for c0, c1 in zip(prev_word, next_word):
            if c0 != c1:
                graph[c0].add(c1)
                break
    return graph


#########################
# Don't change this code
#########################

def get_alphabet(
        words: list[str]
) -> list[str]:
    """
    Extract alphabet from sorted words
    :param words: sorted words
    :return: alphabet
    """
    graph = build_graph(words)
    return extract_alphabet(graph)

#########################
