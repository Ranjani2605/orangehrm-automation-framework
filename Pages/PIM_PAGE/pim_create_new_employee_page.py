import logging

from selenium.webdriver.common.by import By



from Pages.PIM_PAGE.pim_employee_personal_details_page import EmployeePersonalDetailsPage

from Pages.components.breadcrumb_helper import *
class PIMCreateNewEmployeeAdd(PIMBasePage):

    logger = logging.getLogger(__name__)

    #Locators
    add_button = (By.XPATH,"//button[normalize-space()='Add']")
    save_button = (By.XPATH, "//button[normalize-space()='Save']")
    cancel_button = (By.XPATH, "//button[normalize-space()='Cancel']")

    first_name = (By.NAME, "firstName")
    middle_name = (By.NAME, "middleName")
    last_name = (By.NAME, "lastName")
    employee_ID = (By.XPATH, "//label[normalize-space()='Employee Id']/following::input[contains(@class,'oxd-input')][1]")

    breadcrumb_last = (By.CSS_SELECTOR,".oxd-breadcrumb li:last-child")
    topbar_add_employee = (By.XPATH, "//a[contains(@class,'oxd-topbar-body-nav-tab-item') and normalize-space()='Add Employee']")

    # Validation errors
    first_name_required_error = (By.XPATH,
                                 "//input[@id='firstName']/ancestor::div[contains(@class,'oxd-input-group')]"
                                 "//span[contains(@class,'oxd-input-field-error-message') and normalize-space()='Required']"
                                 )

    last_name_required_error = (By.XPATH,
                                "//input[@id='lastName']/ancestor::div[contains(@class,'oxd-input-group')]"
                                "//span[contains(@class,'oxd-input-field-error-message') and normalize-space()='Required']"
                                )
    # Employee list tab
    #expected_tab_bar = (By.XPATH, "//a[normalize-space()='Employee List']")
    expected_tab_bar = (By.XPATH, "//a[normalize-space()='Add Employee']")
    expected_header = (By.XPATH, "//h6[normalize-space()='PIM']")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def assert_on_add_employee_list_page(self, expected_tab_bar=None):
        self.logger.info("verify that the header and tab loaded correctly")
        BreadcrumbHelper(self.driver).assert_breadcrumb_matches_header()
        tab_bar = expected_tab_bar if expected_tab_bar is not None else self.expected_tab_bar
        BreadcrumbHelper(self.driver).verify_tab_bar_text(tab_bar)

    def open_add_employee(self):
        self.logger.info("Open Add Employee form")
        self.click(self.add_button)
        # Some builds require switching via the top tab after clicking Add.
        if not self.is_visible(self.first_name):
            self.click(self.topbar_add_employee)
        self.is_loaded(self.first_name, timeout=10)
        return self

    def get_generated_employee_id(self):
        employee_id_value = self.get_element(self.employee_ID).get_attribute("value").strip()
        assert employee_id_value, "Employee ID was not auto-generated"
        return employee_id_value

    def add_employee(self, first_name, last_name, middle_name=""):
        self.logger.info("Add employee: first=%s, last=%s", first_name, last_name)
        self.open_add_employee()

        self.assert_on_add_employee_list_page()

        self.required_non_empty("first_name", first_name)
        self.required_non_empty("last_name", last_name)

        self.sendkeys(self.first_name, first_name)
        self.sendkeys(self.middle_name, middle_name)
        self.sendkeys(self.last_name, last_name)

        created_employee_id = self.get_generated_employee_id()
        self.click(self.save_button)
        self.logger.info("Employee saved with system-generated ID : %s", created_employee_id)
        return EmployeePersonalDetailsPage(self.driver, created_employee_id=created_employee_id)


    def submit_with_missing_name(self):
        self.logger.info("Submit form with missing first/last name")
        self.open_add_employee()
        self.sendkeys(self.first_name, "")
        self.sendkeys(self.last_name, "")
        self.click(self.save_button)
        return self

    def assert_required_name_error(self):
        self.logger.info("Verify required fields errors for first/last name")
        assert self.is_visible(self.first_name_required_error),"First name required error not shown"
        assert self.is_visible(self.last_name_required_error),"Last name required error not shown"

    def navigate_to_employee_link(self):
        self.logger.info("Navigate to employee personal details")
        self.click(self.employee_list_link)
        return EmployeePersonalDetailsPage(self.driver)

    def required_non_empty(self, field_name, value):
        if value is None or str(value).strip() == "":
            self.logger.info("%s is required", field_name)
            raise ValueError(f"{field_name} must not be empty")



