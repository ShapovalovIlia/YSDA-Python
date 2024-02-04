import heapq
import string


def normalize(
        text: str
) -> str:
    """
    Removes punctuation and digits and convert to lower case
    :param text: text to normalize
    :return: normalized query
    """
    return text.translate(str.maketrans('', '', string.punctuation + string.digits)).lower()


def get_words(
        query: str
) -> list[str]:
    """
    Split by words and leave only words with letters greater than 3
    :param query: query to split
    :return: filtered and split query by words
    """
    return [s for s in query.split() if len(s) > 3]


def build_index(
        banners: list[str]
) -> dict[str, list[int]]:
    """
    Create index from words to banners ids with preserving order and without repetitions
    :param banners: list of banners for indexation
    :return: mapping from word to banners ids
    """
    ans: dict[str, list[int]] = {}
    for i, b in enumerate(banners):
        for s in set(get_words(normalize(b))):
            ans.setdefault(s, []).append(i)
    return ans


def get_banner_indices_by_query(
        query: str,
        index: dict[str, list[int]]
) -> list[int]:
    """
    Extract banners indices from index, if all words from query contains in indexed banner
    :param query: query to find banners
    :param index: index to search banners
    :return: list of indices of suitable banners
    """
    cnt = 0
    qry_word = get_words(normalize(query))
    sorted_indices: list[int] = []

    for w in qry_word:
        if w not in index:
            return []
        index[w].sort()

    heap = [(index[qry_word[i]][0], i) for i in range(len(qry_word)) if index[qry_word[i]]]
    heapq.heapify(heap)
    word_pointers = [0] * len(qry_word)

    while heap:

        if not sorted_indices or sorted_indices[-1] != heap[0][0]:
            while cnt > 0:
                sorted_indices.pop()
                cnt -= 1
            cnt = 1
        else:
            cnt += 1

        sorted_indices.append(heap[0][0])

        if cnt == len(qry_word):
            sorted_indices.append(heap[0][0])
        word_idx = heap[0][1]
        heapq.heappop(heap)
        word_pointers[word_idx] += 1
        if word_pointers[word_idx] < len(index[qry_word[word_idx]]):
            next_tuple = (index[qry_word[word_idx]][word_pointers[word_idx]], word_idx)
            heapq.heappush(heap, next_tuple)

    while cnt > 0:
        sorted_indices.pop()
        cnt -= 1

    return sorted_indices


#########################
# Don't change this code
#########################

def get_banners(
        query: str,
        index: dict[str, list[int]],
        banners: list[str]
) -> list[str]:
    """
    Extract banners matched to queries
    :param query: query to match
    :param index: word-banner_ids index
    :param banners: list of banners
    :return: list of matched banners
    """
    indices = get_banner_indices_by_query(query, index)
    return [banners[i] for i in indices]

#########################
