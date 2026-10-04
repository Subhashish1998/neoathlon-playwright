"""Shared fixtures. pytest-playwright already provides: browser, context, page.

All URLs and credentials come from .env via config/settings.py,
so tests never need them typed in.
"""
import pytest
from playwright.sync_api import expect

from config import settings
from pages.dashboard_page import DashboardPage
from pages.home_page import HomePage
from pages.login_page import LoginPage

expect.set_options(timeout=settings.DEFAULT_TIMEOUT)


# ---- Environment ----
@pytest.fixture(scope="session")
def base_url():
    """BASE_URL from .env. Also lets tests use relative paths: page.goto("/auth")."""
    try:
        return settings.require("BASE_URL")
    except RuntimeError as e:
        pytest.exit(str(e), returncode=4)


@pytest.fixture(scope="session")
def credentials():
    """Valid test user from .env -> {"email": ..., "password": ...}."""
    try:
        return {
            "email": settings.require("TEST_USER_EMAIL"),
            "password": settings.require("TEST_USER_PASSWORD"),
        }
    except RuntimeError as e:
        pytest.fail(str(e), pytrace=False)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, base_url):
    return {
        **browser_context_args,
        "base_url": base_url,
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": True,
    }


@pytest.fixture(autouse=True)
def _default_timeouts(page):
    page.set_default_timeout(settings.DEFAULT_TIMEOUT)
    yield


# ---- Logged-in page ----
@pytest.fixture
def auth_page(browser, browser_context_args, credentials):
    """A page that is already logged in.

    Uses auth/state.json if it exists (fast); otherwise logs in with the
    .env credentials through the UI.
    """
    if settings.AUTH_STATE_FILE.exists():
        context = browser.new_context(
            **browser_context_args, storage_state=str(settings.AUTH_STATE_FILE)
        )
        page = context.new_page()
    else:
        context = browser.new_context(**browser_context_args)
        page = context.new_page()
        LoginPage(page).open().login(credentials["email"], credentials["password"])
        DashboardPage(page).expect_loaded()
    page.set_default_timeout(settings.DEFAULT_TIMEOUT)
    yield page
    context.close()


# ---- Page-object fixtures ----
@pytest.fixture
def home_page(page):
    return HomePage(page)


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page):
    return DashboardPage(page)
