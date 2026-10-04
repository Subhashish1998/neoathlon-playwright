"""Clean a codegen recording so it reads URL and credentials from .env.

Run automatically by record.sh / record.ps1 after you close the browser.
Manual use:  python scripts/clean_recording.py tests/recorded/test_x.py

- page.goto("https://<BASE_URL>/path")   ->  page.goto("/path")
- .fill("<TEST_USER_EMAIL>")             ->  .fill(credentials["email"])
- .fill("<TEST_USER_PASSWORD>")          ->  .fill(credentials["password"])
- adds the `credentials` fixture to the test function when needed
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import settings  # noqa: E402


def clean(code: str) -> str:
    if settings.BASE_URL:
        code = re.sub(
            r'(\.goto\(\s*")' + re.escape(settings.BASE_URL) + r'(/[^"]*)?"',
            lambda m: f'{m.group(1)}{m.group(2) or "/"}"',
            code,
        )
    for key, value in (("email", settings.TEST_USER_EMAIL), ("password", settings.TEST_USER_PASSWORD)):
        if value:
            code = code.replace(f".fill({value!r})", f'.fill(credentials["{key}"])')
            code = code.replace(f'.fill("{value}")', f'.fill(credentials["{key}"])')
    if 'credentials["' in code:
        code = re.sub(
            r"def (test_\w+)\(page: Page\)",
            r"def \1(page: Page, credentials)",
            code,
        )
    return code


def main(path: str) -> None:
    file = Path(path)
    if not file.exists() or not file.read_text(encoding="utf-8").strip():
        print(f"Nothing to clean: {file} is missing or empty (did you close the browser?)")
        return
    original = file.read_text(encoding="utf-8")
    cleaned = clean(original)
    file.write_text(cleaned, encoding="utf-8")
    leftover = [v for v in (settings.TEST_USER_EMAIL, settings.TEST_USER_PASSWORD) if v and v in cleaned]
    print(f"Cleaned {file}" + (" (changes applied)" if cleaned != original else " (nothing to change)"))
    if leftover:
        print("WARNING: credentials still present in the file - check it before committing.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scripts/clean_recording.py <file.py>")
    main(sys.argv[1])
