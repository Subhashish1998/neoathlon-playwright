import pytest


@pytest.mark.smoke
def test_home_page_loads(home_page):
    home_page.open()
    home_page.expect_loaded()
    assert home_page.title() != ""
