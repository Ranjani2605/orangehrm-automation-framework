import time
from datetime import date, datetime, timedelta

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class CalendarHelper(BasePage):

    calendar_widget = (By.XPATH, "//div[contains(@class,'oxd-calendar-wrapper')]")
    # Year dropdown
    year_dropdown = (By.XPATH, "//div[contains(@class,'oxd-calendar-selector-year')]")
    month_dropdown = (By.XPATH, "//div[contains(@class,'oxd-calendar-selector-month')]")

    dropdown_option = (By.XPATH, "//ul[contains(@class,'oxd-calendar-dropdown')]//li[normalize-space()='{value}']")
    day_cell = (By.XPATH, "//div[contains(@class,'oxd-calendar-date') and normalize-space()='{day}']")
    close_link = (By.XPATH, "//div[contains(@class,'oxd-date-input-link') and contains(@class,'--close')]")

    next_btn = (By.XPATH, "//button[contains(@class,'oxd-calendar-next-month')]")
    prev_btn = (By.XPATH, "//button[contains(@class,'oxd-calendar-previous-month')]")


    # Date cells
    calendar_date = (By.XPATH, "//div[@class='oxd-calendar-dates-grid']/div")

    def __init__(self, driver,default_timeout=10):
        super().__init__(driver)
        self.default_timeout = default_timeout

    def wait_for_element(self):
        self.is_visible(self.calendar_widget)
        time.sleep(0.5)

    def select_year(self, year):
        self.click(self.year_dropdown)
        year_option = (By.XPATH, f"//ul[contains(@class,'oxd-calendar-dropdown')]//li[normalize-space()='{year}']")
        self.click(year_option)

    def select_month(self, month):
        self.click(self.month_dropdown)
        month_options = (By.XPATH,f"//ul[contains(@class,'oxd-calendar-dropdown')]//li[normalize-space()='{month}']")
        self.click(month_options)

    def select_day(self, day):
        day_locator = (By.XPATH, f"//div[contains(@class,'oxd-calendar-date') and normalize-space()='{day}']")
        self.click(day_locator)


    def select_date(self, year, month, day):
        self.select_year(year)
        self.select_month(month)
        self.select_day(day)
        try:
            self.click(self.close_link)
        except Exception:
            pass

        time.sleep(0.5)

