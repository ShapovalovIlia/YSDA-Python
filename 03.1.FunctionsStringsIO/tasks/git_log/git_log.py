import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """
    for i in inp:
        ans = str()
        lst = i.split('\t')
        ans += lst[0][:7]
        comment = lst[4].strip('\n')
        ans = ans.ljust(80 - len(comment), '.')
        ans += comment + '\n'
        out.write(ans)
