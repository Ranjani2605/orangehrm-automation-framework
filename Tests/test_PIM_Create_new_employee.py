import json
import os

import allure
import pytest

from Pages.PIM_PAGE.pim_create_new_employee_page import PIMCreateNewEmployeeAdd
from Pages.PIM_PAGE.pim_employee_list import PIMEmployeeList
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
    left_sidebar.navigate_to_pim()
    new_employee = PIMCreateNewEmployeeAdd(driver)


    created_employee = new_employee.add_employee(
        first_name=emp_data["first_name"],
        middle_name=emp_data.get("middle_name", ""),
        last_name=emp_data["last_name"],

    )

    created_employee_id = created_employee.employee_id

    created_employee.added_additional_details(
        day=emp_data["day"],
        month=emp_data["month"],
        year=emp_data["year"],
        nationality=emp_data["nationality"],
        marital_status=emp_data["marital_status"],
        birth_year=emp_data["birth_year"],
        birth_month=emp_data["birth_month"],
        birth_day=emp_data["birth_day"],
        gender=emp_data["gender"]


    )

    left_sidebar.navigate_to_pim()
    employee_list = PIMEmployeeList(driver)
    employee_list.search_by_employee_id(created_employee_id)
    employee_list.validate_exist_employee_id(created_employee_id)





