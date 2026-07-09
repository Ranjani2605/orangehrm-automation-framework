from urllib.parse import urlparse

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from constants.constants import Constants
from locators.dashboard_locators.dashboard_locators import (
    DashboardLocators,
    leave_empty_message,
    quick_launch_button,
    widget_by_title,
    widget_canvas,
    widget_chart_legend_labels,
)


class DashboardPage(BasePage):
    PAGE_URL = Constants.APP_DASHBOARD_URL
    PAGE_LOAD_TIMEOUT = 20
    EXPECTED_WIDGET_TITLES = (
        "Time at Work",
        "My Actions",
        "Quick Launch",
        "Buzz Latest Posts",
        "Employees on Leave Today",
        "Employee Distribution by Sub Unit",
        "Employee Distribution by Location",
    )
    QUICK_LAUNCH_URLS = {
        "Assign Leave": Constants.APP_LEAVE_URL,
        "Leave List": Constants.APP_LEAVE_URL,
        "Timesheets": Constants.APP_TIME_URL,
        "Apply Leave": Constants.APP_LEAVE_URL,
        "My Leave": Constants.APP_LEAVE_URL,
        "My Timesheet": Constants.APP_TIME_URL,
    }
    VALID_TIME_STATES = {"Punched In", "Punched Out"}

    def open(self):
        self.driver.get(self.PAGE_URL)
        return self.wait_until_loaded()

    def wait_until_loaded(self, timeout=None):
        wait_time = timeout if timeout is not None else max(self.default_timeout, self.PAGE_LOAD_TIMEOUT)
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(DashboardLocators.DASHBOARD_GRID)
        )
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: len(driver.find_elements(*DashboardLocators.DASHBOARD_WIDGETS)) >= 1
        )
        return self

    def _wait_for_visible(self, locator, timeout=None):
        wait_time = timeout if timeout is not None else self.default_timeout
        last_error = None
        for _ in range(3):
            try:
                return WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_element_located(locator)
                )
            except StaleElementReferenceException as error:
                last_error = error
        if last_error:
            raise last_error
        raise TimeoutException(f"Element was not visible for locator: {locator}")

    def _wait_for_all_visible(self, locator, timeout=None):
        wait_time = timeout if timeout is not None else self.default_timeout
        last_error = None
        for _ in range(3):
            try:
                return WebDriverWait(self.driver, wait_time).until(
                    EC.visibility_of_all_elements_located(locator)
                )
            except StaleElementReferenceException as error:
                last_error = error
        if last_error:
            raise last_error
        raise TimeoutException(f"Elements were not visible for locator: {locator}")

    def _get_text(self, locator, timeout=None):
        return self._wait_for_visible(locator, timeout).text.strip()

    def _current_path(self):
        return urlparse(self.driver.current_url).path

    def wait_for_url(self, expected_url, timeout=None):
        wait_time = timeout if timeout is not None else self.default_timeout
        expected_path = urlparse(expected_url).path
        WebDriverWait(self.driver, wait_time).until(EC.url_contains(expected_path))
        return self.driver.current_url

    def is_widget_visible(self, widget_title, timeout=None):
        return self.is_visible(widget_by_title(widget_title), timeout=timeout or 5)

    def get_widget_titles(self):
        return [
            title.text.strip()
            for title in self._wait_for_all_visible(DashboardLocators.DASHBOARD_WIDGET_TITLES)
            if title.text.strip()
        ]

    def get_time_at_work_state(self):
        return self._get_text(DashboardLocators.TIME_AT_WORK_STATE)

    def get_time_at_work_details(self):
        return self._get_text(DashboardLocators.TIME_AT_WORK_DETAILS)

    def get_time_at_work_duration(self):
        return self._get_text(DashboardLocators.TIME_AT_WORK_TODAY_DURATION)

    def is_time_at_work_action_enabled(self):
        return self._wait_for_visible(DashboardLocators.TIME_AT_WORK_ACTION_BUTTON).is_enabled()

    def click_time_at_work_action(self):
        self.click(DashboardLocators.TIME_AT_WORK_ACTION_BUTTON)
        return self

    def wait_for_time_state(self, expected_state, timeout=None):
        wait_time = timeout if timeout is not None else self.default_timeout
        WebDriverWait(self.driver, wait_time).until(
            lambda driver: self.get_time_at_work_state() == expected_state
        )
        return self.get_time_at_work_state()

    def get_my_actions(self):
        actions = []
        for item in self._wait_for_all_visible(DashboardLocators.MY_ACTION_ITEMS):
            label = item.find_element(*DashboardLocators.MY_ACTION_TEXT).text.strip()
            button = item.find_element(*DashboardLocators.MY_ACTION_BUTTON)
            actions.append(
                {
                    "label": label,
                    "enabled": button.is_enabled(),
                }
            )
        return actions

    def get_quick_launch_titles(self):
        return [
            title.text.strip()
            for title in self._wait_for_all_visible(DashboardLocators.QUICK_LAUNCH_HEADINGS)
            if title.text.strip()
        ]

    def open_quick_launch_tile(self, tile_name):
        if not tile_name or tile_name not in self.QUICK_LAUNCH_URLS:
            raise ValueError(f"Unsupported quick launch tile: {tile_name!r}")
        self.click(quick_launch_button(tile_name))
        self.wait_for_url(self.QUICK_LAUNCH_URLS[tile_name])
        return self.driver.current_url

    def get_buzz_posts(self):
        posts = []
        for card in self._wait_for_all_visible(DashboardLocators.BUZZ_POST_CARDS):
            posts.append(
                {
                    "author": card.find_element(*DashboardLocators.BUZZ_POST_AUTHOR).text.strip(),
                    "timestamp": card.find_element(*DashboardLocators.BUZZ_POST_TIME).text.strip(),
                    "body": card.find_element(*DashboardLocators.BUZZ_POST_BODY).text.strip(),
                }
            )
        return posts

    def is_leave_empty_state_visible(self):
        return self.is_visible(DashboardLocators.LEAVE_EMPTY_STATE, timeout=3)

    def is_leave_empty_image_visible(self):
        return self.is_visible(DashboardLocators.LEAVE_EMPTY_IMAGE, timeout=3)

    def get_leave_empty_message(self):
        return self._get_text(
            leave_empty_message("Employees on Leave Today"),
            timeout=3,
        )

    def is_chart_canvas_visible(self, widget_title):
        return self.is_visible(widget_canvas(widget_title), timeout=5)

    def get_chart_legend_labels(self, widget_title):
        labels = self._wait_for_all_visible(
            widget_chart_legend_labels(widget_title),
            timeout=5,
        )
        return [label.text.strip() for label in labels if label.text.strip()]
