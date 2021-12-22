import pytest
import requests
from scrape.scrape import _get_web_page_as_soup, _confirm_webpage, download_from_site, get_target_tag, _get_filename

@pytest.fixture
def url():
    return "https://google.com"


def test_page_exists():
    page = url()
    r = requests.get(page, allow_redirects=True)
    assert r.status_code == 200



if __name__ == "__main__":
    pytest.main()