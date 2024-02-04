import typing as tp
import heapq


def merge(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    heap: list[tuple[int, bytes, int]] = []

    for i, stream in enumerate(input_streams):
        line = stream.readline()
        if line:
            value = int(line)
            heapq.heappush(heap, (value, line, i))

    while heap:
        hooinya, value_bytes, index = heapq.heappop(heap)
        output_stream.write(value_bytes)

        line = input_streams[index].readline()
        if line:
            next_value = int(line)
            heapq.heappush(heap, (next_value, line, index))
