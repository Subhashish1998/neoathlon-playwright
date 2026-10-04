# Neoathlon Web Automation (Playwright + Pytest)

## 1. Setup (once)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate     macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
copy .env.example .env      # cp on macOS/Linux
```
Open `.env` and set your real values. **Everything is read from `.env`**, so you never type a URL, email or password in a test.

| Key | Meaning |
|---|---|
| `BASE_URL` | App URL, no trailing slash |
| `LOGIN_PATH` | Login route, e.g. `/auth` |
| `TEST_USER_EMAIL` / `TEST_USER_PASSWORD` | Valid test account |
| `DEFAULT_TIMEOUT` | Action/assertion timeout in ms |

`.env` is git-ignored. Only `.env.example` (dummy values) is committed.

## 2. Structure
```
neoathlon-playwright/
├── config/settings.py        reads .env (BASE_URL, credentials, timeouts)
├── pages/                    Page Objects
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_page.py
│   └── dashboard_page.py
├── tests/
│   ├── smoke/                fast critical-path tests   (-m smoke)
│   ├── regression/           full suite                 (-m regression)
│   └── recorded/             raw codegen output         (-m recorded)
├── data/users.json           dummy test data (invalid users etc.)
├── utils/data_loader.py
├── scripts/                  codegen helpers (read BASE_URL from .env)
├── conftest.py               fixtures: base_url, credentials, auth_page, page objects
├── .env.example              template - copy to .env
├── pytest.ini
└── requirements.txt
```
Created at runtime (git-ignored): `reports/`, `test-results/`, `auth/state.json`.

## 3. Using .env values in tests
```python
def test_something(page, credentials):
    page.goto("/")                                   # BASE_URL is prepended automatically
    page.get_by_role("textbox", name="Email").fill(credentials["email"])
    page.get_by_role("textbox", name="Password").fill(credentials["password"])
```
Need to start already logged in? Use the `auth_page` fixture.

## 4. Record with codegen
```powershell
.\scripts\record.ps1 signup /signup          # Windows
./scripts/record.sh  signup /signup          # Git Bash / macOS / Linux
```
Writes `tests/recorded/test_signup.py`. Use **Assert text / Assert visibility** in the toolbar
(turn the button on *before* clicking the element).

When you close the browser, the script **automatically cleans the file**
(`scripts/clean_recording.py`): the URL becomes a relative path and the email/password you typed
become `credentials["email"]` / `credentials["password"]` from `.env`.
Type the **same** email/password that are in `.env` while recording so they get replaced.

See `tests/recorded/test_login_recorded.py` for an example.

Save a logged-in session once (optional, speeds up `auth_page`):
```powershell
.\scripts\record_login.ps1        # log in, close the browser -> auth/state.json
```

## 5. Turn a recording into a proper test
1. Run it: `pytest tests/recorded/test_signup.py --headed`
2. Move locators into a page object (`pages/signup_page.py`).
3. Add a fixture in `conftest.py`, write the clean test in `tests/smoke` or `tests/regression`.
4. Delete the raw recording.

## 6. Run
```bash
pytest                         # all
pytest -m smoke                # smoke only
pytest -m regression
pytest --headed --slowmo 500   # watch it
pytest -n 4                    # parallel
pytest --reruns 2              # retry flaky tests
```
Report: `reports/report.html`. Failures keep screenshot, video and trace in `test-results/`:
```bash
playwright show-trace test-results/<test>/trace.zip
```
