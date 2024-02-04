from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Directory to save your .json files to
# NB: create this directory if it doesn't exist
SAVED_JSON_DIR = Path(__file__).parent / 'visited_paths'


def distance(source_url: str, target_url: str) -> int | None:
    """Amount of wiki articles which should be visited to reach the target one
    starting from the source url. Assuming that the next article is choosing
    always as the very first link from the first article paragraph (tag <p>).
    If the article does not have any paragraph tags or any links in the first
    paragraph then the target is considered unreachable and None is returned.
    If the next link is pointing to the already visited article, it should be
    discarded in favor of the second link from this paragraph. And so on
    until the first not visited link will be found or no links left in paragraph.
    NB. The distance between neighbour articles (one is pointing out to the other)
    assumed to be equal to 1.
    :param source_url: the url of source article from wiki
    :param target_url: the url of target article from wiki
    :return: the distance calculated as described above
    """
    visited = set()
    page = requests.get(source_url)
    cur = source_url
    dist: int = 0
    test_titles: set[str] = {x.name.replace('_', ' ') for x in (Path(__file__).parent / 'testdata').iterdir()}
    while True:
        if cur == target_url:
            return dist
        dist += 1
        visited.add(cur)
        to_page = None
        soup = BeautifulSoup(page.text, "html.parser")

        content = soup.find('div', class_='mw-parser-output')
        if content:
            first_paragraph = content.find('p', recursive=False)
            if first_paragraph:
                links = first_paragraph.find_all('a', href=True)
                for link in links:
                    if link.get('title') is None or link.get('title') not in test_titles:
                        continue
                    url = 'https://ru.wikipedia.org' + link['href']
                    if url in visited:
                        continue
                    if not link.get('href').startswith('/wiki'):
                        continue
                    if url.startswith('https://ru.wikipedia.org/wiki/'):
                        visited.add(url)
                        cur = url
                        to_page = requests.get(url)
                        break
        if to_page is None:
            break
        page = to_page
    return None
