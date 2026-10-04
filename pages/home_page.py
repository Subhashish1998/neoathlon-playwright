from playwright.sync_api import expect

from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    def __init__(self, page):
        super().__init__(page)
        self.body = page.locator("body")
        self.start_journey = page.get_by_role("link", name="Start Your Journey")

    def expect_loaded(self):
        expect(self.body).to_be_visible()

    def go_to_login(self):
        self.start_journey.click()
