import re

import requests
from bs4 import BeautifulSoup, SoupStrainer

BASE_URL = "https://man7.org/linux/man-pages/"
ALL_MAN_PAGE = "https://man7.org/linux/man-pages/dir_all_by_section.html"


def parse_page(url: str, filter_tag: str = None) -> BeautifulSoup:
    response = requests.get(url)
    html = response.text
    return BeautifulSoup(html, "lxml", parse_only=SoupStrainer(filter_tag))


def get_man_page_urls(url: str = ALL_MAN_PAGE) -> list:
    soup = parse_page(url, filter_tag="a")
    hrefs = [link.get("href") for link in soup if link.has_attr("href")]
    match_refs = [re.search(r"man\d/.+.html$", ref) for ref in hrefs]
    return [BASE_URL + ref.group() for ref in match_refs if ref]


if __name__ == "__main__":
    print(get_man_page_urls())
