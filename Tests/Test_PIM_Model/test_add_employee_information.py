import allure

from pages.PIM_PAGE.pim_create_new_employee_page import PIMCreateNewEmployeeAdd
from pages.PIM_PAGE.pim_employee_list import PIMEmployeeList
from pages.left_sidebar_page import LeftSidebarPage


@allure.title("Add employee")
@allure.description("Add the new employee")
def test_add_employee(authenticated_driver, test_data):
    emp_data = test_data["create_new_employee"]
    left_sidebar = LeftSidebarPage(authenticated_driver)
    left_sidebar.navigate_to_pim()

    employee_add = PIMCreateNewEmployeeAdd(authenticated_driver)
    created_employee = employee_add.add_employee(
        first_name=emp_data["first_name"],
        middle_name=emp_data.get("middle_name", ""),
        last_name=emp_data["last_name"],
    )

    created_employee.added_additional_details(
        day=emp_data["day"],
        month=emp_data["month"],
        year=emp_data["year"],
        nationality=emp_data["nationality"],
        marital_status=emp_data["marital_status"],
        birth_year=emp_data["birth_year"],
        birth_month=emp_data["birth_month"],
        birth_day=emp_data["birth_day"],
        gender=emp_data["gender"],
    )

    employee_list = PIMEmployeeList(authenticated_driver)
    employee_list.search_by_employee_id(created_employee.employee_id)

    assert employee_list.validate_exist_employee_id(created_employee.employee_id) is not None

