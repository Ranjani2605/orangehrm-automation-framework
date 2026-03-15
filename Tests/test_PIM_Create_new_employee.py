import json
import os

import allure
import pytest

from Pages.left_sidebar_page import LeftSidebarPage
from Utilities.auth import login


@allure.title("Add employee")
@allure.description("Add the new employee")
def test_add_employee(driver):
    login(driver)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "Utilities", "data.json")

    print(f"Looking for file {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    with open(file_path) as file:
        data = json.load(file)

    emp_data = data["create_new_employee"]

    left_sidebar = LeftSidebarPage(driver)
    pim_page = left_sidebar.navigate_to_pim()

    first_name = emp_data["first_name"]
    middle_name = emp_data.get("middle_name", "")
    last_name = emp_data["last_name"]
    employee_id = emp_data.get("employee_id", "")

    pim_page.add_employee(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        employee_id=employee_id
    )
