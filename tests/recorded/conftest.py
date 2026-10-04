import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if "tests/recorded" in item.nodeid.replace("\\", "/"):
            item.add_marker(pytest.mark.recorded)
