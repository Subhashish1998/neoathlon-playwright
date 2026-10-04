# neoathlon-playwright
Record browser tests by just clicking through a website. Playwright codegen writes the test script for you: no coding needed to get started. Python + Pytest, with your URL and login read from a .env file.
# Playwright Codegen Test Automation

Automate any website just by clicking through it. No coding needed to get started.

This project uses **Playwright codegen** to record what you do in the browser
(clicks, typing, navigation) and turn it into a ready-to-run test script.
Anyone can use it: open the site, perform the steps, add a check
(like "Dashboard is visible"), close the browser, and the test is saved for you.

## Why use it
- 🖱️ **Record by clicking.** Codegen writes the script automatically.
- ✅ **Add checks visually.** Use "Assert text" / "Assert visibility" while recording.
- 🔒 **No secrets in code.** Website URL, email and password live in your own `.env` file, never in Git.
- 🧹 **Auto clean-up.** Recorded scripts are rewritten to read URL and login details from `.env`.
- 🗂️ **Organised suites.** `smoke`, `regression` and `recorded` tests, plus Page Objects for reuse.
- 📊 **Reports included.** HTML report, plus screenshot, video and trace when a test fails.

## Quick start (Git Bash)
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env              # add your website URL and test login

./scripts/record.sh login /auth   # click through the site, then close the browser
pytest tests/recorded/test_login.py --headed
```

Works with any website: just change `BASE_URL` in `.env`.
