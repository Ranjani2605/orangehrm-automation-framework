import allure
import pytest
from pages.add_employee_page import AddEmployeePage
from pages.employee_list_page import EmployeeListPage
from pages.personal_details_page import PersonalDetailsPage
from pages.pim_page import PimPage

@allure.epic("OrangeHRM")
@allure.feature("PIM Employee Management")
class TestPimEmployee:
    def create_employee(self, driver, employee):
        pim_page = PimPage(driver)
        add_employee_page = AddEmployeePage(driver)
        personal_details_page = PersonalDetailsPage(driver)
        pim_page.navigate_to_pim()
        pim_page.open_add_employee()
        assert add_employee_page.is_add_employee_page_displayed(), "Add Employee page not displayed"
        employee_id = add_employee_page.add_employee(
            first_name=employee["first_name"],
            middle_name=employee.get("middle_name", ""),
            last_name=employee["last_name"]
        )
        assert personal_details_page.is_personal_details_page_displayed(), (
            "Personal Details page was not displayed after saving employee"
        )
        return employee_id
    @pytest.mark.smoke
    @pytest.mark.pim
    @allure.title("User can navigate to PIM module")
    def test_user_can_navigate_to_pim_module(self, authenticated_driver):
        pim_page = PimPage(authenticated_driver)
        pim_page.navigate_to_pim()

        assert pim_page.is_pim_page_displayed(), "PIM page was not displayed"

        @pytest.mark.regression
        @pytest.mark.pim
        @allure.title("User can add employee with mandatory fields")
        def test_user_can_add_employee_with_mandatory_fields(
                self,
                authenticated_driver,
                employee_data,
                unique_employee
        ):
            mandatory_employee = {
                "first_name": unique_employee["first_name"],
                "last_name": unique_employee["last_name"]
            }
            employee_id = self.create_employee(authenticated_driver, mandatory_employee)
            assert employee_id.strip() != "", "Employee ID should not be empty"

        @pytest.mark.regression
        @pytest.mark.pim
        @allure.title("User can add employee with first, middle and last name")
        def test_user_can_add_employee_with_full_name(self, authenticated_driver, unique_employee):
            employee_id = self.create_employee(authenticated_driver, unique_employee)
            assert employee_id.strip() != "", "Employee ID should not be empty"

        @pytest.mark.regression
        @pytest.mark.pim
        @allure.title("Employee ID is auto-generated and not empty")
        def test_employee_id_is_auto_generated_and_not_empty(self, authenticated_driver):
            pim_page = PimPage(authenticated_driver)
            add_employee_page = AddEmployeePage(authenticated_driver)
            pim_page.navigate_to_pim()
            pim_page.open_add_employee()
            employee_id = add_employee_page.get_employee_id()
            assert employee_id.strip() != "", "Employee ID was not auto-generated"

        @pytest.mark.regression
        @pytest.mark.pim
        @allure.title("User can search employee by employee ID")
        def test_user_can_search_employee_by_employee_id(self, authenticated_driver, unique_employee):
            employee_id = self.create_employee(authenticated_driver, unique_employee)
            pim_page = PimPage(authenticated_driver)
            employee_list_page = EmployeeListPage(authenticated_driver)
            pim_page.navigate_to_pim()
            pim_page.open_employee_list()
            employee_list_page.search_by_employee_id(employee_id)
            assert employee_list_page.is_employee_present_in_results(employee_id), (
                f"Employee ID {employee_id} was not found in search results"
            )

        @pytest.mark.regression
        @pytest.mark.pim
        @allure.title("User can search employee by employee name")
        def test_user_can_search_employee_by_employee_name(self, authenticated_driver, unique_employee):
            self.create_employee(authenticated_driver, unique_employee)
            pim_page = PimPage(authenticated_driver)
            employee_list_page = EmployeeListPage(authenticated_driver)
            pim_page.navigate_to_pim()
            pim_page.open_employee_list()
            employee_list_page.search_by_employee_name(unique_employee["first_name"])
            assert employee_list_page.is_employee_present_in_results(unique_employee["first_name"]), (
                f"Employee name {unique_employee['first_name']} was not found in search results"
            )

        @pytest.mark.regression
        @pytest.mark.pim
        @allure.title("Employee details are displayed correctly in employee table")
        def test_employee_details_are_displayed_in_employee_table(
                self,
                authenticated_driver,
                unique_employee
        ):
            employee_id = self.create_employee(authenticated_driver, unique_employee)
            pim_page = PimPage(authenticated_driver)
            employee_list_page = EmployeeListPage(authenticated_driver)
            pim_page.navigate_to_pim()
            pim_page.open_employee_list()
            employee_list_page.search_by_employee_id(employee_id)
            first_result_text = employee_list_page.get_first_result_text()
            assert employee_id in first_result_text
            assert unique_employee["first_name"] in first_result_text
            assert unique_employee["last_name"] in first_result_text

        @pytest.mark.regression
        @pytest.mark.pim
        @allure.title("User can edit employee personal details")
        def test_user_can_edit_employee_personal_details(
                self,
                authenticated_driver,
                unique_employee,
                edited_employee
        ):
            self.create_employee(authenticated_driver, unique_employee)
            personal_details_page = PersonalDetailsPage(authenticated_driver)
            personal_details_page.update_employee_name(
                first_name=edited_employee["first_name"],
                middle_name=edited_employee["middle_name"],
                last_name=edited_employee["last_name"]
            )
            assert personal_details_page.is_success_message_displayed(), (
                "Success message was not displayed after updating personal details"
            )
            assert personal_details_page.get_first_name_value() == edited_employee["first_name"]
            assert personal_details_page.get_middle_name_value() == edited_employee["middle_name"]
            assert personal_details_page.get_last_name_value() == edited_employee["last_name"]

        @pytest.mark.validation
        @pytest.mark.pim
        @allure.title("Required field messages are displayed on Add Employee page")
        def test_required_field_messages_are_displayed_on_add_employee_page(
                self,
                authenticated_driver,
                login_data
        ):
            pim_page = PimPage(authenticated_driver)
            add_employee_page = AddEmployeePage(authenticated_driver)
            expected_message = login_data["messages"]["required"]
            pim_page.navigate_to_pim()
            pim_page.open_add_employee()
            add_employee_page.click_save()
            required_messages = add_employee_page.get_required_error_messages()
            assert expected_message in required_messages

