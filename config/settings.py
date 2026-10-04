"""Central configuration. Every value comes from .env (or real environment variables).

Nothing secret or environment-specific is hard-coded here: set it in .env.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env", override=True)  # .env always wins

BASE_URL = os.getenv("BASE_URL", "").strip().rstrip("/")
LOGIN_PATH = os.getenv("LOGIN_PATH", "/auth").strip()
TEST_USER_EMAIL = os.getenv("TEST_USER_EMAIL", "").strip()
TEST_USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "")
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "15000"))

AUTH_STATE_FILE = ROOT_DIR / "auth" / "state.json"
DATA_DIR = ROOT_DIR / "data"


def require(name: str) -> str:
    """Return a required setting or raise a clear error telling you what to add to .env."""
    value = globals().get(name) or ""
    if not value:
        raise RuntimeError(
            f"{name} is not set. Add it to your .env file "
            f"(copy .env.example to .env and fill in real values)."
        )
    return value
