import logging
import re
import subprocess as sp
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path

import requests
from bs4 import BeautifulSoup, SoupStrainer

from src.utils import write_csv

BASE_URL = "https://man7.org/linux/man-pages/"
ALL_MAN_PAGE = "https://man7.org/linux/man-pages/dir_all_by_section.html"
URL_PATTERN = r"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"


def parse_web_page(url: str, filter_tag: str = None) -> BeautifulSoup:
    """Given URL returns Beuatiful Soup object to scrap further"""
    html = ""
    try:
        response = requests.get(url, timeout=(5, 6))
        html = response.text
    except Exception as e:
        logging.error(f"Request to page {url} failed with error: {e.args}")
    return BeautifulSoup(html, "lxml", parse_only=SoupStrainer(filter_tag))


def get_man_page_urls(url: str = ALL_MAN_PAGE) -> list:
    """Specific method to find all man page html page link"""
    soup = parse_web_page(url, filter_tag="a")
    hrefs = [link.get("href") for link in soup if link.has_attr("href")]
    match_refs = [re.search(r"man\d/.+.html$", ref) for ref in hrefs]
    return [BASE_URL + ref.group() for ref in match_refs if ref]


def save_man_page_urls(path: str = "data/man_page_urls.csv") -> None:
    urls = get_man_page_urls()
    write_csv(
        path,
        [
            dict(
                command=re.search(r"[^/]+$", url).group().split(".")[0],
                man_page_url=url,
            )
            for url in urls
        ],
    )


def get_man_entry(command: str) -> str:
    """Executes man command to fetch man page entry"""
    if not command:
        return None
    try:
        man_entry = sp.check_output(
            ["man", command],
            timeout=5,
            text=True,
        )
        filter_output = sp.check_output(
            ["col", "-b"],
            input=man_entry,
            timeout=5,
            text=True,
        )
        return filter_output
    except sp.SubprocessError as e:
        logging.debug(f"Failed to get man page for {command} with error: {e.args}")
        return None


def parse_single_tldr(page: Path) -> dict:
    command = page.name.replace(".md", "")
    man_entry = get_man_entry(command)
    tldr_summary = page.read_text()
    doc_url = get_doc_url(tldr_summary)
    doc_text = parse_web_page(doc_url).text if doc_url else None
    return dict(
        command=command,
        doc_url=doc_url,
        doc_text=doc_text,
        man_entry=man_entry,
        tldr_summary=tldr_summary,
    )


def generate_tech_summary_data(path: str = "tldr_repo/pages/") -> None:
    """Extracts command, tldr summary and man page entry"""

    path = Path(path)
    for tldr_path in path.iterdir():
        tldr_pages = list(tldr_path.glob("*.md"))
        with ThreadPoolExecutor(max_workers=5) as executor:
            summary_data = list(executor.map(parse_single_tldr, tldr_pages))
        write_csv(f"data/summary/{tldr_path.name}.csv", summary_data)


def get_doc_url(tldr_summary: str) -> str or None:
    match = re.search(URL_PATTERN, tldr_summary)
    return match.group() if match else None


if __name__ == "__main__":
    # save_man_page_urls()
    generate_tech_summary_data()
