from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class PIMBasePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.Success_message = (By.XPATH, "//h1[@id='profile-pic-header']/following::span[1]")

    def verify_success_message(self, expected=None):
        if expected is None:
            expected = "Successfully saved"
        actual_message = self.get_text(self.Success_message)
        assert actual_message == expected, f"Expected {expected}, but got {actual_message}"
        self.logger.info(f"Verified success message: '{actual_message}'")
        return self
