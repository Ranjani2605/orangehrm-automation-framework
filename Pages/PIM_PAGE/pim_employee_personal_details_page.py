import logging

from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class EmployeePersonalDetailsPage(BasePage):
    logger = logging.getLogger(__name__)

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

    def month_option(self, month):
        return(
            By.XPATH,
            f"//div[contains(@class,'oxd-calendar-calendar-month')]//li[normalize-space()='{month}']"
        )

    def year_option(self, year):
        return(
            By.XPATH,
            f"//div[contains(@class,'oxd-calendar-selector-year')]//li[normalize-space()='{year}']"
        )

    def day_option(self, day):
        return(
            By.XPATH,
            f"//div[contains(@class,'oxd-calendar-dates-grid')]//div[contains(@class,'oxd-calendar-date') and normalize-space()='{int(day)}']"
        )

    def open_calendar(self, field_locator):
        self.logger.info("Open calendar for %s", field_locator)
        self.click(field_locator)
        assert self.is_visible(self.calendar), "Calendar did not open"
        return self

    def select_calendar_date(self, field_locator, year, month, day):
            self.logger.info("Select date %s-%s-%s", year, month, day)
            self.open_calendar(field_locator)
            try:
                self.click(self.month_open)
            except Exception:
                self.open_calendar(field_locator)
                self.click(self.month_open)
            self.click(self.month_option(month))
            try:
                self.click(self.year_open)
            except Exception:
                self.open_calendar(field_locator)
                self.click(self.year_open)
            self.click(self.year_option(str(year)))
            try:
                self.click(self.day_option(day))
            except Exception:
                self.open_calendar(field_locator)
                self.click(self.day_option(day))
            return self

    def set_license_expiry_date(self, year, month, day):
        return self.select_calendar_date(self.license_exp_date, year, month, day)

    def set_date_of_birth(self, year, month, day):
        return self.select_calendar_date(self.dob, year, month, day)

    def select_nationality(self, nationality):
        self.logger.info("Select nationality: %s", nationality)
        self.select_dropdown(self.nationality_dd, nationality)
        return self

    def select_marital_status(self, marital_status):
        self.logger.info("Select marital status: %s", marital_status)
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










