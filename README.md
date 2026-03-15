# POM-Framework

Selenium + Pytest Page Object Model (POM) framework targeting the OrangeHRM demo site.
Includes page classes, test suites, and utilities for configuration, logging, and Allure reporting.

## Tech stack
- Python
- Pytest
- Selenium WebDriver
- Allure (pytest plugin)

## Project structure
- `Pages/`: page objects and base page helpers
- `Tests/`: test cases and fixtures
- `Utilities/`: config, logging, screenshots, and test data
- `config/`: INI-based configuration
- `constants/`: URL constants for OrangeHRM routes
- `reports/`, `screenshots/`, `logs/`: runtime artifacts (if enabled)

## Setup
1) Create and activate a virtual environment.
2) Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
You can set runtime values via environment variables or a `.env` file.

Supported variables (used by `Utilities/config.py`):
- `BASE_URL`
- `ADMIN_USER`
- `ADMIN_PASSWORD`
- `TIMEOUT`

There is a sample `.env` at `Utilities/.env` you can copy or mirror at the repo root if you prefer.
Default values are also in `config/config.ini`.

## Running tests
Run all tests:
```bash
pytest Tests
```

Run a single test file:
```bash
pytest Tests/test_login.py
```

## Allure reporting (optional)
Generate Allure results:
```bash
pytest --alluredir=allure-results Tests
```

Serve the report (requires Allure CLI installed):
```bash
allure serve allure-results
```

## Notes
- Test data lives in `Utilities/data.json`.
- Login and admin test flows target the OrangeHRM demo site.
