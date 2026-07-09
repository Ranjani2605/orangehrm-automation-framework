# POM Framework

Selenium, Pytest, Page Object Model, Allure, and CI examples for OrangeHRM UI automation.

The framework is intentionally simple: page objects contain locators/actions/queries, tests contain assertions, and shared concerns live in fixtures or small utilities.

## Setup

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Configuration

Runtime values can be supplied through environment variables, `Utilities/.env`, root `.env`, or `config/<env>.env`.

Supported values:

```text
ENV=qa
BASE_URL=https://opensource-demo.orangehrmlive.com
APP_PATH=/web/index.php/auth/login
ORANGEHRM_USERNAME=Admin
ORANGEHRM_PASSWORD=admin123
BROWSER=chrome
HEADLESS=false
EXPLICIT_WAIT=20
PAGE_LOAD_TIMEOUT=30
```

## Running Tests

```bash
pytest
pytest --browser chrome
pytest --browser edge
pytest --browser firefox
pytest --browser chrome --env qa --headless
pytest Tests/test_login.py
```

Allure results are written to `allure-results` by default.

```bash
allure serve allure-results
```

## Fixture Strategy

Session scope:

- `environment_config`: environment and URL values
- `browser_config`: browser and headless mode
- `test_data`: shared JSON test data
- `allure_environment`: Allure environment details

Module scope:

- `driver`: creates one browser per module
- `authenticated_driver`: login once before module tests and logout after module tests

Function scope:

- `test_logging`: logs test start/completion
- `pytest_runtest_makereport`: screenshots, browser logs, and current URL on failure

Preferred flow:

```text
Login
├── Test Case 1
├── Test Case 2
├── Test Case 3
└── Logout
```

Use raw `driver` only for tests that need to validate login or unauthenticated behaviour.

## Improvements Made

| Current issue | Risk / impact | Improved implementation | Reasoning |
| --- | --- | --- | --- |
| Chrome was created directly inside fixtures/tests. | Cross-browser runs and CI setup were inconsistent. | `Utilities/browser_factory.py` centralises Chrome, Edge, and Firefox creation using WebDriverManager. | One place controls browser options, page load timeout, and headless mode. |
| Feature tests logged in before every test. | Slow execution and more flaky failures around authentication. | `authenticated_driver` logs in once per module and logs out during module teardown. | Matches enterprise regression execution where setup cost is shared safely within a module. |
| Test data was loaded repeatedly with hard-coded paths. | Duplicate code and broken paths in nested test folders. | `test_data` session fixture loads `Utilities/data.json` once. | Easier onboarding and fewer path mistakes. |
| Wait logic was duplicated and some methods used broad exceptions. | Timeouts were hidden or inconsistent. | `Utilities/wait_utils.py` and `BasePage` provide reusable explicit wait wrappers. | Stable waits make failures clearer and reduce flaky timing issues. |
| `time.sleep()` was used in PIM date handling. | Fixed waits slow tests and still fail on slow pages. | Replaced sleep with a wait for the calendar widget. | Waits follow application state instead of elapsed time. |
| Assertions existed in some page objects. | Page methods mixed actions and test decisions. | Page validation helpers now return booleans where changed. | Tests own assertions; page objects remain reusable. |
| Logging created timestamped files with a bad date format and duplicate handlers. | Hard to find the active run log; repeated handlers duplicate log lines. | `logs/automation.log` is configured once. | Predictable log location for CI artifacts and local debugging. |
| Failure evidence was manual. | Failed CI runs lacked useful diagnostics. | Pytest hook attaches screenshots, browser logs, and current URL to Allure. | Faster triage without rerunning locally. |
| Route constants ignored configured environments. | Dev/qa/staging/prod support was partial. | Constants derive URLs from `BASE_URL`. | Same tests can target different environments. |
| CI examples were missing. | Teams had to invent pipeline steps. | Added GitHub Actions, Azure DevOps, and Jenkins examples. | Gives a practical baseline for enterprise CI/CD. |

## Project Structure

```text
Pages/                  Page objects and reusable page components
Tests/                  Pytest suites and shared conftest fixtures
Utilities/              Browser factory, waits, config, logging, screenshots
constants/              Environment-aware application route constants
locators/               Page locator modules
allure-results/         Runtime Allure results
logs/automation.log     Runtime framework log
```

## CI/CD

Examples are included:

- `.github/workflows/ui-tests.yml`
- `azure-pipelines.yml`
- `Jenkinsfile`

Pipelines install Python dependencies, run headless tests, generate Allure results, and archive logs/reports.
