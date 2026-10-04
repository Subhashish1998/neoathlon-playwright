"""Login page. Locators taken from the codegen recording."""
from playwright.sync_api import expect

from config import settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = settings.LOGIN_PATH  # from .env (LOGIN_PATH), default /auth

    def __init__(self, page):
        super().__init__(page)
        self.email = page.get_by_role("textbox", name="Email")
        self.password = page.get_by_role("textbox", name="Password")
        self.submit = page.get_by_role("button", name="Sign In")
        self.error = page.get_by_role("alert")  # TODO: confirm the real error locator

    def login(self, email: str, password: str):
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
        return self

    def expect_error(self):
        expect(self.error).to_be_visible()
