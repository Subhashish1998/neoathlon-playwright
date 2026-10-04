"""Raw codegen recording, cleaned up to read URL and credentials from .env.

After recording a new test, do the same:
  - replace "https://..." with a relative path, e.g. page.goto("/")
    (BASE_URL from .env is added automatically)
  - replace typed email/password with credentials["email"] / credentials["password"]
"""
from playwright.sync_api import Page, expect


def test_login_recorded(page: Page, credentials) -> None:
    page.goto("/")
    page.get_by_role("link", name="Start Your Journey").click()
    page.get_by_role("textbox", name="Email").fill(credentials["email"])
    page.get_by_role("textbox", name="Password").fill(credentials["password"])
    page.get_by_role("button", name="Sign In").click()

    dashboard = page.get_by_role("link", name="Dashboard")
    expect(dashboard).to_be_visible()
    expect(dashboard).to_have_text("Dashboard")
