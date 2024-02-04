import pyarrow as pa
import pyarrow.parquet as pq

ValueType = int | list[int] | str | dict[str, str]


def save_rows_to_parquet(rows: list[dict[str, ValueType]], output_filepath: str) -> None:
    """
    Save rows to parquet file.

    :param rows: list of rows containing data.
    :param output_filepath: local filepath for the resulting parquet file.
    :return: None.
    """
    types: dict[type, pa.types] = {
        int: pa.int64(),
        str: pa.string(),
        list: pa.list_(pa.int64()),
        dict: pa.map_(pa.string(), pa.string())
    }
    schemes = []
    has: dict[str, type] = dict()
    cnt: dict[str, int] = dict()
    for rw in rows:
        for k, v in rw.items():
            if has.get(k) is None:
                has[k] = type(v)
                cnt[k] = 1
            else:
                cnt[k] += 1
            if has[k] != type(v):
                raise TypeError(f'Field {k} has different types')
    for k in has:
        schemes.append(pa.field(k, types[has[k]], (cnt[k] != len(rows))))
    table = pa.Table.from_pylist(rows, pa.schema(schemes))
    pq.write_table(table, output_filepath)
