import logging
import time

from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from Pages.PIM_PAGE.PIM_BASE_PAGE import PIMBasePage
from Pages.base_page import BasePage
from Pages.components.calendar_helper import CalendarHelper


class EmployeePersonalDetailsPage(PIMBasePage, BasePage):

    logger = logging.getLogger(__name__)

    # select license expire date
    click_License_expiry_date = (By.XPATH, "(//i[@class='oxd-icon bi-calendar oxd-date-input-icon'])[1]")
    click_Date_of_birth = (By.XPATH, "(//i[@class='oxd-icon bi-calendar oxd-date-input-icon'])[2]")
    # Input fields (label-based locators for new UI)
    license_exp_date = (By.XPATH, "//label[normalize-space()='License Expiry Date']/following::input[contains(@class,'oxd-input')][1]")
    dob = (By.XPATH, "//label[normalize-space()='Date of Birth']/following::input[contains(@class,'oxd-input')][1]")

    # Dropdowns / selectors
    dropdown_nationality = (By.XPATH,"//label[text()='Nationality']/following::div[contains(@class,'oxd-select-text')][1]")
    listbox_nationality = (By.XPATH, "//div[@role='listbox']")
    marital_status_dd = (By.ID, "personal_cmbMarital")
    blood_type_dd = (By.ID, "custom_1_4")

    # Gender (new UI radio group) + legacy ids
    gender_group = (By.XPATH, "//label[normalize-space()='Gender']/following::div[contains(@class,'oxd-radio-group') or @role='radiogroup'][1]")
    gender_male = (By.ID, "personal_optGender_1")
    gender_female = (By.ID, "personal_optGender_2")

    # Actions
    save_btn = (By.XPATH, "(//button[@type='submit'])[1]")
    attachment_file = (By.ID, "frmElmtContainer")
    attach_add_btn = (By.XPATH, "//input[@value='Add']")

    # loading overlays (blocks clicks)
    loading_overlay = (By.XPATH, "//div[contains(@class,'oxd-form-loader') or contains(@class,'oxd-loading-spinner-container')]")

    # Validation
    required_error = (By.XPATH, "//span[normalize-space()='Required']")


    # Calendar (custom OrangeHRM control)
    calendar = (By.XPATH, "//div[contains(@class,'oxd-calendar-wrapper')]")
    month_open = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-month')]//div[contains(@class,'oxd-calendar-selector-month-selected')]")
    year_open = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-year')]//div[contains(@class,'oxd-calendar-selector-year-selected')]")


    # Success employee created
    successfully_saved = (By.XPATH, "//div[contains(@class,'oxd-toast-content') and .//p[normalize-space()='Successfully Saved']]")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.calendar_helper = CalendarHelper(driver)

    def set_license_expiry_date(self, year, month, day):
        self.logger.info("Updated the license expiry date of employee")
        self.wait_for_invisibility(self.loading_overlay, timeout=20)
        field = self.get_element(self.license_exp_date, timeout=20)
        scroll_y = self.driver.execute_script("return window.pageYOffset;")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
        try:
            field.click()
        except ElementClickInterceptedException:
            self.wait_for_invisibility(self.loading_overlay, timeout=20)
            self.driver.execute_script("arguments[0].click();", field)
        time.sleep(0.3)
        self.calendar_helper.select_date(year, month, day)
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        self.driver.execute_script("window.scrollTo(0, arguments[0]);", scroll_y)
        self.wait_for_invisibility(self.loading_overlay, timeout=10)
        return self

    def set_date_of_birth(self, birth_year, birth_month, birth_day):
        self.logger.info("update the date of birth of employee")
        self.wait_for_invisibility(self.loading_overlay, timeout=15)
        field = self.get_element(self.dob, timeout=15)
        scroll_y = self.driver.execute_script("return window.pageYOffset;")

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", field)
        self.driver.execute_script("arguments[0].click();", field)

        self.get_element(self.calendar, timeout=10)
        self.calendar_helper.select_date(birth_year, birth_month, birth_day)
        self.driver.execute_script("window.scrollTo(0, arguments[0]);", scroll_y)
        self.wait_for_invisibility(self.loading_overlay, timeout=10)
        return self

    def select_nationality(self, nationality):
        self.logger.info("Select nationality: %s", nationality)
        self.click(self.dropdown_nationality)
        self.is_visible(self.listbox_nationality, timeout=10)
        option_nationality = f".//span[normalize-space()='{nationality}']"
        listbox_element = self.driver.find_element(*self.listbox_nationality)
        option_element = listbox_element.find_element(By.XPATH, option_nationality)
        option_element.click()
        return self

    def select_marital_status(self, marital_status):
        self.logger.info("Select marital status: %s", marital_status)
        self.select_oxd_dropdown("Marital Status", marital_status)
        return self

    def select_gender(self, gender):
        gender_value = gender.strip().lower()
        if gender_value not in ("male", "female"):
            raise ValueError("Gender must be 'male' or 'female'")
        label = "Male" if gender_value == "male" else "Female"

        self.wait_for_invisibility(self.loading_overlay, timeout=10)
        option = self.get_element((By.XPATH, f"//label[normalize-space()='{label}']//span[contains(@class,'oxd-radio-input')]"),
                                  timeout=10
                                  )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", option)
        self.driver.execute_script("arguments[0].click();", option)
        self.logger.info("Selected gender: %s", label)
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


    def successfully_added_employee(self, success):
        self.logger.info("Successfully added employee: %s", success)
        element = self.is_visible(self.successfully_saved)
        actual_text = element.text

        assert actual_text == "Successfully Saved", \
        f"Expected 'Successfully Saved' but got '{actual_text}'"
