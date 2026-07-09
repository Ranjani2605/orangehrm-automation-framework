import logging

from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from Utilities.config_reader import Config
from Utilities.wait_utils import WaitUtils


logger = logging.getLogger(__name__)

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config
from Utilities.logger import get_logger


class BasePage:
    """
    Common Selenium actions used by all page classes.
    Tests should call page methods, not raw Selenium directly.
    """
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.DEFAULT_TIMEOUT)
        self.logger = get_logger(self.__class__.__name__)

    def open_url(self, url):
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_all_visible(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator):
        self.logger.info(f"Clicking element: {locator}")
        self.wait_for_clickable(locator).click()

    def enter_text(self, locator, text, clear_first=True):
        self.logger.info(f"Entering text into element: {locator}")
        element = self.wait_for_visible(locator)

        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        text = self.wait_for_visible(locator).text
        self.logger.info(f"Text from {locator}: {text}")
        return text

    def get_attribute(self, locator, attribute_name):
        value = self.wait_for_visible(locator).get_attribute(attribute_name)
        self.logger.info(f"Attribute {attribute_name} from {locator}: {value}")
        return value

    def is_visible(self, locator):
        try:
            self.wait_for_visible(locator)
            return True
        except TimeoutException:
            return False

    def get_elements(self, locator):
        return self.driver.find_elements(*locator)

    def wait_for_url_contains(self, partial_url):
        self.logger.info(f"Waiting for URL to contain: {partial_url}")
        return self.wait.until(EC.url_contains(partial_url))

    def scroll_to_element(self, locator):
        element = self.wait_for_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def press_enter(self, locator):
        self.wait_for_visible(locator).send_keys(Keys.ENTER)

    def move_to_element(self, locator):
        element = self.wait_for_visible(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def get_current_url(self):
        return self.driver.current_url
















