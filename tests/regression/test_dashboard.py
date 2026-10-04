import pytest

from pages.dashboard_page import DashboardPage


@pytest.mark.regression
@pytest.mark.auth
def test_dashboard_visible_when_logged_in(auth_page):
    DashboardPage(auth_page).expect_loaded()
