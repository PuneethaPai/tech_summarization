import pytest

from src.generate_data import get_doc_url, parse_single_tldr
from pathlib import Path


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", None),
        ("simpole", None),
        ("https://google.com", "https://google.com"),
        (
            "star something http://www.youtube.com then end with something",
            "http://www.youtube.com",
        ),
    ],
)
def test_get_doc_url(text, expected):
    assert get_doc_url(text) == expected


@pytest.mark.parametrize(
    "path, cmd, url",
    [
        ("7z.md", "7z", "https://www.7-zip.org/"),
        ("ab.md", "ab", "https://httpd.apache.org/docs/2.4/programs/ab.html"),
        ("arch.md", "arch", None),
        # ("alias.md", "alias", None),
        # TODO: arch and alias man entryies are messed up example:
        # The a\x08ar\x08rc\x08ch\x08h command with no arguments == The arch command with no arguments
    ],
)
def test_parse_single_man_page(path, cmd, url):
    base_path = "tldr_repo/pages/common"
    result = parse_single_tldr(base_path / Path(path))
    assert result["command"] == cmd
    assert result["doc_url"] == url
    assert result["man_entry"] == None or cmd in result["man_entry"]
    assert cmd in result["tldr_summary"]
