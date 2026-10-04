"""Login edge cases. Invalid users live in data/users.json (dummy data only)."""
import pytest

from utils.data_loader import load_json


@pytest.mark.regression
@pytest.mark.skip(reason="TODO: confirm the error-message locator in LoginPage.error")
def test_login_with_invalid_credentials(login_page):
    user = load_json("users.json")["invalid_user"]
    login_page.open()
    login_page.login(user["email"], user["password"])
    login_page.expect_error()
