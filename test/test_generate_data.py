import pytest

from src.generate_data import get_doc_url


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
