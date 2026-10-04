"""Dashboard (landing page after a successful login)."""
from playwright.sync_api import expect

from pages.base_page import BasePage


class DashboardPage(BasePage):
    PATH = "/dashboard"  # TODO: confirm the real dashboard route

    def __init__(self, page):
        super().__init__(page)
        self.dashboard_link = page.get_by_role("link", name="Dashboard")

    def expect_loaded(self):
        expect(self.dashboard_link).to_be_visible()
        expect(self.dashboard_link).to_have_text("Dashboard")
