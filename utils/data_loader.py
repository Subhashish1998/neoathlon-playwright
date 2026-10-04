import json

from config.settings import DATA_DIR


def load_json(name: str):
    """Load a test-data file from data/, e.g. load_json('users.json')."""
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)
