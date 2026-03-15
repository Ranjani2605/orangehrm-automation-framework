import logging

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from config.config_reader import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
logger = logging.getLogger(__name__)



class BasePage:

    def __init__(self, driver, default_timeout=10):
        self.driver = driver
        self.default_timeout = default_timeout
        self.wait = WebDriverWait(driver, self.default_timeout)
        self.logger = logger


    def is_loaded(self, locator, timeout=None):
        try:
            wait_time = timeout if timeout is not None else self.default_timeout
            WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def click(self, locator, timeout=None):
        logger.info(f"Clicking: {locator}")
        wait_time = timeout if timeout is not None else self.default_timeout
        element = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))
        element.click()

    def presence_of_element(self, locator, timeout=None):
        wait_time = timeout if timeout is not None else self.default_timeout
        WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))

    def sendkeys(self, locator, text ,timeout=10):
        try:
            wait_time = timeout if timeout is not None else self.default_timeout
            type_field = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
            type_field.send_keys(text)
        except TimeoutException:
            raise  Exception (f"Element not visible for locator : {locator}")

    def get_text(self, locator, timeout=None):
        try:
            wait_time = timeout if timeout is not None else self.default_timeout
            get_field = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
            return get_field.text
        except:
            return None

    def select_dropdown(self, locator,text_field,timeout=None):
        try:
            wait_time = timeout if timeout is not None else self.default_timeout
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
            dropdown = Select(element)
            dropdown.select_by_visible_text(text_field)

        except TimeoutException:
            raise Exception(f"Element not loaded")

    def is_visible(self, locator, timeout=10):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_disappear(self, locator, timeout=5):
        """Wait for toast/success message to disappear"""
        self.wait.until(EC.presence_of_element_located(locator))


    def find_all_elements(self, locator):
        self.wait.until(EC.visibility_of_all_elements_located(locator))


    def get_element(self, dropdown_locator, timeout=15):
        wait_time = timeout if timeout is not None else self.default_timeout
        return WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(dropdown_locator))


    def press_enter(self, locator, timeout=10):
        wait_time = timeout if timeout is not None else self.default_timeout
        element = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
        element.send_keys(Keys.ENTER)

    def find_all(self, locator):
        self.wait.until(EC.presence_of_all_elements_located(locator))

    def verify_page_title(self, expected_title):
        actual_title = self.driver.title
        assert actual_title == expected_title, f"Expected '{expected_title}', but got '{actual_title}'"
        return True






