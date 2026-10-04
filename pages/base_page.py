"""Base class every page object inherits from."""
import re

from playwright.sync_api import Page, expect

from config import settings


class BasePage:
    # Path relative to BASE_URL, overridden in each page, e.g. "/auth"
    PATH = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(f"{settings.require('BASE_URL')}{self.PATH}")
        return self

    def title(self) -> str:
        return self.page.title()

    def expect_url_contains(self, fragment: str):
        expect(self.page).to_have_url(re.compile(re.escape(fragment)))

    def screenshot(self, name: str):
        self.page.screenshot(path=f"test-results/{name}.png", full_page=True)
