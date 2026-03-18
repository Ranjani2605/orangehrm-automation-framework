import logging

from selenium.webdriver.common.by import By

from Pages.PIM_PAGE.PIM_BASE_PAGE import PIMBasePage
from Pages.base_page import BasePage
from Pages.components.calendar_helper import CalendarHelper


class EmployeePersonalDetailsPage(PIMBasePage):

    logger = logging.getLogger(__name__)

    # select license expirey date
    click_License_expiry_date = (By.XPATH, "(//i[contains(@class,'bi-calendar')])[1]")
    click_Date_of_birth = (By.XPATH, "(//i[contains(@class,'bi-calendar')])[2]")
    # Input fields
    license_exp_date = (By.NAME, "licenseExpiryDate")
    dob = (By.NAME, "dateOfBirth")

    # Dropdowns / selectors
    nationality_dd = (By.ID, "personal_cmbNationality")
    marital_status_dd = (By.ID, "personal_cmbMarital")
    blood_type_dd = (By.ID, "custom_1_4")

    # Gender
    gender_male = (By.ID, "personal_optGender_1")
    gender_female = (By.ID, "personal_optGender_2")

    # Actions
    save_btn = (By.ID, "btnSave")
    attachment_file = (By.ID, "frmElmtContainer")
    attach_add_btn = (By.XPATH, "//input[@value='Add']")

    # Validation
    required_error = (By.XPATH, "//span[normalize-space()='Required']")

    # Calendar (custom OrangeHRM control)
    calendar = (By.XPATH, "//div[contains(@class,'oxd-calendar-wrapper')]")
    month_open = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-month')]//div[contains(@class,'oxd-calendar-selector-month-selected')]")
    year_open = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-year')]//div[contains(@class,'oxd-calendar-selector-year-selected')]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.calendar = CalendarHelper(driver)

    def set_license_expiry_date(self, year, month, day):
        self.logger.info("Updated the license expiry date of employee")
        self.is_loaded(self.license_exp_date, timeout=15)
        self.click(self.click_License_expiry_date)
        self.calendar.select_date_month_year(year, month, day)
        return self

    def set_date_of_birth(self, birth_year, birth_month, birth_day):
        self.logger.info("update the date of birth of employee")
        self.is_loaded(self.dob, timeout=10)
        self.click(self.click_Date_of_birth)
        self.calendar.select_date_month_year(birth_year, birth_month, birth_day)
        return self

    def select_nationality(self, nationality):
        self.logger.info("Select nationality: %s", nationality)
        self.select_dropdown(self.nationality_dd, nationality)
        return self

    def select_marital_status(self, marital_status):
        self.logger.info("Select marital status: %s", marital_status)
        self.select_dropdown(self.marital_status_dd, marital_status)
        return self

    def select_gender(self, gender):
        gender_value = gender.strip().lower()
        if gender_value == "male":
            self.click(self.gender_male)
        elif gender_value == "female":
            self.click(self.gender_female)
        else:
            raise ValueError("Gender must be 'male' or 'female'")
        self.logger.info("Gender must be 'male' or 'female'")
        return self

    def select_blood_type(self, blood_type):
        self.logger.info("Select blood type: %s", blood_type)
        self.select_dropdown(self.blood_type_dd, blood_type)
        return self

    def upload_attachment(self, file_path):
        self.logger.info("Upload attachment: %s", file_path)
        attachment_file = self.get_element(self.attachment_file)
        self.click(attachment_file)
        return self

    def save_personal_details(self):
        self.logger.info("Save personal details")
        self.click(self.save_btn)
        return self

    def assert_required_error_visible(self):
        self.logger.info("Verify required validation error is visible")
        assert self.is_visible(self.required_error), "Required validation error is not visible"
        return self


    def added_additional_details(self, day, month, year, nationality,marital_status,
                                 birth_year, birth_month, birth_day,gender ):
        self.set_license_expiry_date(year, month, day)
        self.select_nationality(nationality)
        self.select_marital_status(marital_status)
        self.set_date_of_birth(birth_year, birth_month, birth_day)
        self.select_gender(gender)
        self.click(self.save_btn)
        return self








