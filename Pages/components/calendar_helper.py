from datetime import date, datetime, timedelta

from selenium.webdriver.common.by import By

from Pages.base_page import BasePage


class CalendarHelper(BasePage):
    # Year dropdown
    year_label = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-year')]//div[contains(@class,'oxd-calendar-selector-year-selected')]")
    year_dropdown_toggle = (By.XPATH, "//li[contains(@class,'oxd-calendar-selector-year')]//div[contains(@class,'oxd-calendar-selector-year-selected')]")
    calendar_year_dropdown = (By.XPATH, "//ul[@role='menu']//li")

    # Month navigation
    month_label = (By.XPATH, "//div[@class='oxd-calendar-selector-month-selected']")
    forward_tab = (By.XPATH, "//i[@class='oxd-icon bi-chevron-right']")
    back_tab = (By.XPATH, "//button[@class='oxd-icon-button']//i[@class='oxd-icon bi-chevron-left']")

    # Date cells
    calendar_date = (By.XPATH, "//div[@class='oxd-calendar-dates-grid']/div")

    def __init__(self, driver):
        super().__init__(driver)

    def get_future_date(self, day_ahead: int = 0) -> date:
        return date.today() + timedelta(days=day_ahead)

    def get_future_date_str(self, day_ahead: int = 0, fmt: str = "%Y-%m-%d") -> str:
        target = self.get_future_date(day_ahead)
        return target.strftime(fmt)

    def click_date_cell(self, day: int):
        cells = self.driver.find_elements(*self.calendar_date)
        for cell in cells:
            if cell.text.strip() == str(day):
                cell.click()
                return
        raise AssertionError(f"Day '{day}' not found in calendar grid")

    def select_year(self, year: int):
        self.click(self.year_dropdown_toggle)
        options = self.driver.find_elements(*self.calendar_year_dropdown)
        if not options:
            raise AssertionError("Year dropdown did not open or has no options")
        years = [int(opt.text.strip()) for opt in options if opt.text.strip().isdigit()]
        if not years:
            raise AssertionError("Year dropdown options were not numeric")
        min_year, max_year = min(years), max(years)
        if year < min_year or year > max_year:
            raise AssertionError(f"Year '{year}' not in dropdown range {min_year}-{max_year}")
        for opt in options:
            if opt.text.strip() == str(year):
                opt.click()
                return
        raise AssertionError(f"Year '{year}' not found in calendar dropdown")

    def select_month(self, month):
        if isinstance(month, int):
            target_month = datetime.strptime(str(month), "%m").strftime("%B")
        else:
            target_month = str(month)

        for _ in range(12):
            current_month = (self.get_text(self.month_label) or "").strip()
            if current_month == target_month:
                return
            current_idx = datetime.strptime(current_month, "%B").month if current_month else 1
            target_idx = datetime.strptime(target_month, "%B").month
            if current_idx < target_idx:
                self.click(self.forward_tab)
            else:
                self.click(self.back_tab)
        raise AssertionError(f"Month '{target_month}' not found after 12 steps")

    def select_date_month_year(self, year, month, day):
        self.select_year(year)
        self.select_month(month)
        self.click_date_cell(day)
