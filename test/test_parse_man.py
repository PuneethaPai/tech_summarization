import random

import pytest
import requests

from src.generate_data import get_man_page_urls


def test_get_man_page_urls(capsys):
    all_man_pages = get_man_page_urls()
    assert len(all_man_pages) == 11267
    resp = requests.get(random.choice(all_man_pages))
    assert resp.status_code == 200
