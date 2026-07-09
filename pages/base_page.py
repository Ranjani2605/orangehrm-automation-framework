import logging

from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from Utilities.config_reader import Config
from Utilities.wait_utils import WaitUtils


logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver, default_timeout=None):
        self.driver = driver
        self.default_timeout = default_timeout or Config.EXPLICIT_WAIT
        self.waits = WaitUtils(driver, self.default_timeout)
        self.wait = WebDriverWait(driver, self.default_timeout)
        self.logger = logger

    def is_loaded(self, locator, timeout=None):
        return self.waits.is_visible(locator, timeout)

    def click(self, locator, timeout=None):
        logger.info("Clicking element: %s", locator)
        element = self.waits.until_clickable(locator, timeout)
        element.click()
        return element

    def presence_of_element(self, locator, timeout=None):
        return self.waits.until_present(locator, timeout)

    def sendkeys(self, locator, text, timeout=None):
        try:
            field = self.waits.until_visible(locator, timeout)
            field.clear()
            field.send_keys(text)
            return field
        except TimeoutException as error:
            raise TimeoutException(
                f"Element not visible for locator: {locator}"
            ) from error

    def type_text(self, locator, text, timeout=None):
        return self.sendkeys(locator, text, timeout)

    def get_text(self, locator, timeout=None):
        try:
            return self.waits.until_visible(locator, timeout).text
        except TimeoutException:
            return None

    def select_dropdown(self, locator, text_field, timeout=None):
        try:
            element = self.waits.until_present(locator, timeout)
            Select(element).select_by_visible_text(text_field)
            return self
        except TimeoutException as error:
            raise TimeoutException(f"Dropdown not loaded: {locator}") from error

    def select_oxd_dropdown(self, label_text, option_text, timeout=None):
        dropdown = (
            "xpath",
            f"//label[normalize-space()='{label_text}']"
            "/following::div[contains(@class,'oxd-select-text')][1]",
        )
        option = (
            "xpath",
            f"//div[@role='listbox']//span[normalize-space()='{option_text}']",
        )
        self.click(dropdown, timeout)
        self.click(option, timeout)
        return self

    def is_visible(self, locator, timeout=None):
        return self.waits.is_visible(locator, timeout)

    def wait_for_disappear(self, locator, timeout=None):
        return self.wait_for_invisibility(locator, timeout)

    def find_all_elements(self, locator):
        return self.waits.until_all_visible(locator)

    def find_all(self, locator):
        return self.waits.until_all_present(locator)

    def find_element(self, locator):
        return self.waits.until_present(locator)

    def get_element(self, locator, timeout=None):
        return self.waits.until_visible(locator, timeout)

    def press_enter(self, locator, timeout=None):
        element = self.waits.until_visible(locator, timeout)
        element.send_keys(Keys.ENTER)
        return self

    def verify_page_title(self, expected_title):
        return self.driver.title == expected_title

    def wait_for_invisibility(self, locator, timeout=None):
        return self.waits.until_invisible(locator, timeout)
