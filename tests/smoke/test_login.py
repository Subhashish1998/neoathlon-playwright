"""Valid login lands on the dashboard. Email/password come from .env."""
import pytest


@pytest.mark.smoke
def test_login_lands_on_dashboard(home_page, login_page, dashboard_page, credentials):
    home_page.open()
    home_page.go_to_login()
    login_page.login(credentials["email"], credentials["password"])
    dashboard_page.expect_loaded()
