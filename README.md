File type: markdown
# OrangeHRM Selenium Python Pytest Automation Framework
## Project Overview
This is a UI automation framework built for the OrangeHRM demo application using Python, Selenium 
WebDriver, Pytest, Page Object Model, JSON test data, Allure reporting, GitHub Actions and Jenkins.
The goal of this project is to demonstrate practical QA automation skills for QA Automation Engineer / 
Automation Test Engineer roles in the UK.
## Tech Stack- Python- Selenium WebDriver- Pytest- Page Object Model- JSON test data- Explicit waits- Allure reporting- Logging- Screenshot capture on failure- GitHub Actions- Jenkins
## Framework Features- Clean Page Object Model design- Reusable Selenium actions in BasePage- Test data separated into JSON files- Pytest fixtures for browser setup and login- CLI options for browser and headless mode- Explicit waits instead of time.sleep- Screenshot capture on test failure- Allure result generation- GitHub Actions pipeline- Jenkins pipeline- Smoke, regression, validation and module-level Pytest markers
## Test Scenarios Covered
1. Valid login
2. Invalid login
3. Login with blank username
4. Login with blank password
5. Dashboard page validation
6. Navigate to PIM module
7. Add employee with mandatory fields
8. Add employee with first, middle and last name
9. Validate employee ID is auto-generated / not empty
10. Search employee by employee ID
11. Search employee by employee name
12. Verify employee details in employee table
13. Edit employee personal details
14. Validate required field error messages
15. Logout successfully
## Folder Structure
orangehrm-selenium-python-pytest-framework/
|-- config/
|   `-- config.py
|-- pages/
|   |-- base_page.py
|   |-- login_page.py
|   |-- dashboard_page.py
|   |-- pim_page.py
|   |-- add_employee_page.py
|   |-- employee_list_page.py
|   `-- personal_details_page.py
|-- tests/
|   |-- test_login.py
|   |-- test_dashboard.py
|   |-- test_pim_employee.py
|   `-- test_logout.py
|-- test_data/
|   |-- login_data.json
|   `-- employee_data.json
|-- utilities/
|   |-- data_reader.py
|   |-- logger.py
|   `-- screenshot.py
|-- reports/
|-- screenshots/
|-- logs/
|-- .github/
|   `-- workflows/
|       `-- tests.yml
|-- conftest.py
|-- pytest.ini
|-- requirements.txt
|-- Jenkinsfile
|-- README.md
`-- .gitignore
## Setup Instructions
### Clone the repository
git clone https://github.com/YOUR_USERNAME/orangehrm-selenium-python-pytest-framework.git
cd orangehrm-selenium-python-pytest-framework
### Create virtual environment
python -m venv .venv
### Activate virtual environment on Windows PowerShell
.\.venv\Scripts\Activate.ps1
### Install dependencies
pip install -r requirements.txt
## Test Execution Commands
Run all tests:
pytest
Run tests in headed Chrome:
pytest --browser chrome
Run tests in headless Chrome:
pytest --browser chrome --headless
Run smoke tests:
pytest -m smoke
Run regression tests:
pytest -m regression
Run login tests:
pytest -m login
Run PIM tests:
pytest -m pim
## Allure Report
Run tests with Allure results:
pytest --alluredir=allure-results
Open Allure report:
allure serve allure-results
Note: Allure command-line tool and Java must be installed separately to open the HTML report.
## CI/CD
GitHub Actions workflow file:
.github/workflows/tests.yml
Jenkins pipeline file:
Jenkinsfile
## Screenshots
Failure screenshots are saved under:
screenshots/
Screenshots are also attached to Allure reports when tests fail.
## What This Project Demonstrates- Python Selenium automation- Page Object Model design- Pytest fixtures and markers
- UI test automation for HR workflows
-  Positive and negative test scenarios
-  Form validation testing
-  Dynamic employee test data
-  Search and table validation
-  Screenshot capture on failure
- Allure reporting
- GitHub Actions and Jenkins CI/CD exposure