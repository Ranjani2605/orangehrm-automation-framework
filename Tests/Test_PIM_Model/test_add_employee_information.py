import json
import os

import allure
import pytest

from Pages.PIM_PAGE.pim_create_new_employee_page import PIMCreateNewEmployeeAdd
from Pages.system_users_page import SystemUsersPage
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

    emp_data = data["add_employee"]


    employee_add = PIMCreateNewEmployeeAdd(driver)
    employee_add.add_new_employee(select_role=emp_data['select_role'],
                                  employee_name=emp_data['employee_name'],
                                  select_status=emp_data['select_status'],
                                  username=emp_data['username'],
                                  password=emp_data['password'],
                                  confirm_password=emp_data['confirm_password']
                                  )

    system_users = SystemUsersPage(driver)
    system_users.search_employee_by_name(emp_data['employee_name'])

    assert system_users.verify_user_record(
        username=emp_data['username'],
        user_role=emp_data['select_role'],
        employee_name=emp_data['employee_name'],
        status=emp_data['select_status'],
    )





