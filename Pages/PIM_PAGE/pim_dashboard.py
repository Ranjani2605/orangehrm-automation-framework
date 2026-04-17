from selenium.webdriver.common.by import By

from Pages.components.table_helper import TableHelper


class PIMDashboard(TableHelper):
    employee_name = (
        By.XPATH,
        "//label[normalize-space()='Employee Name']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    employee_id = (
        By.XPATH,
        "//label[normalize-space()='Employee Id']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    dropdown_employment_status = (
        By.XPATH,
        "//label[normalize-space()='Employment Status']/ancestor::div[contains(@class,'oxd-input-group')]"
        "//i[contains(@class,'caret')]",
    )
    employment_status_value = (
        By.XPATH,
        "//label[normalize-space()='Employment Status']/ancestor::div[contains(@class,'oxd-input-group')]"
        "//div[contains(@class,'oxd-select-text-input')]",
    )
    employee_record = (
        By.XPATH,
        "//label[normalize-space()='Include']/ancestor::div[contains(@class,'oxd-input-group')]"
        "//i[contains(@class,'caret')]",
    )
    employee_record_value = (
        By.XPATH,
        "//label[normalize-space()='Include']/ancestor::div[contains(@class,'oxd-input-group')]"
        "//div[contains(@class,'oxd-select-text-input')]",
    )
    supervisor_name = (
        By.XPATH,
        "//label[normalize-space()='Supervisor Name']/ancestor::div[contains(@class,'oxd-input-group')]//input",
    )
    job_title = (
        By.XPATH,
        "//label[normalize-space()='Job Title']/ancestor::div[contains(@class,'oxd-input-group')]"
        "//i[contains(@class,'caret')]",
    )
    job_title_value = (
        By.XPATH,
        "//label[normalize-space()='Job Title']/ancestor::div[contains(@class,'oxd-input-group')]"
        "//div[contains(@class,'oxd-select-text-input')]",
    )
    sub_unit = (
        By.XPATH,
        "//label[normalize-space()='Sub Unit']/ancestor::div[contains(@class,'oxd-input-group')]"
        "//i[contains(@class,'caret')]",
    )
    sub_unit_value = (
        By.XPATH,
        "//label[normalize-space()='Sub Unit']/ancestor::div[contains(@class,'oxd-input-group')]"
        "//div[contains(@class,'oxd-select-text-input')]",
    )
    reset_button = (By.XPATH, "//button[normalize-space()='Reset']")
    search_button = (By.XPATH, "//button[normalize-space()='Search']")
    no_records_found = (By.XPATH, "//p[normalize-space()='No Records Found']")

    DEFAULT_DROPDOWN_VALUES = {
        "employment_status": "-- Select --",
        "job_title": "-- Select --",
        "sub_unit": "-- Select --",
    }

    TABLE_HEADER_ALIASES = {
        "employee_id": ("Employee Id", "Employee ID", "Id"),
        "employment_status": ("Employment Status",),
        "job_title": ("Job Title",),
        "sub_unit": ("Sub Unit",),
        "supervisor_name": ("Supervisor", "Supervisor Name"),
    }

    @staticmethod
    def normalize(value):
        return " ".join(str(value).strip().lower().split())

    def type(self, locator, value):
        element = self.get_element(locator)
        element.clear()
        element.send_keys(value)

    def get_input_value(self, locator):
        return self.get_element(locator).get_attribute("value").strip()

    def get_dropdown_value(self, locator):
        return self.get_text(locator).strip()

    def get_row_text(self, row_data):
        return self.normalize(" ".join(str(value) for value in row_data.values()))

    def get_row_value(self, row_data, aliases):
        normalized_aliases = {self.normalize(alias) for alias in aliases}
        for header, value in row_data.items():
            if self.normalize(header) in normalized_aliases:
                return value.strip()
        return None

    def row_matches_expected(self, row_data, expected_values):
        for field_name, expected_value in expected_values.items():
            if not expected_value or field_name == "employee_record":
                continue

            normalized_expected = self.normalize(expected_value)

            if field_name == "employee_name":
                if normalized_expected not in self.get_row_text(row_data):
                    return False
                continue

            aliases = self.TABLE_HEADER_ALIASES.get(field_name, ())
            actual_value = self.get_row_value(row_data, aliases)

            if actual_value is None:
                if normalized_expected not in self.get_row_text(row_data):
                    return False
                continue

            if self.normalize(actual_value) != normalized_expected:
                return False

        return True

    def select_dropdown_option(self, value):
        selected_value = (
            By.XPATH,
            f"//div[@role='option'][normalize-space()='{value}']"
            f"|//div[@role='option']//span[normalize-space()='{value}']",
        )
        self.click(selected_value, timeout=5)

    def enter_employee_name(self, employee_name):
        self.type(self.employee_name, employee_name)

    def enter_employee_id(self, employee_id):
        self.type(self.employee_id, str(employee_id))

    def select_employment_status(self, status):
        self.click(self.dropdown_employment_status)
        self.select_dropdown_option(status)

    def select_employee_record(self, record):
        self.click(self.employee_record)
        self.select_dropdown_option(record)

    def enter_supervisor_name(self, supervisor_name):
        self.type(self.supervisor_name, supervisor_name)

    def select_job_title(self, job_title):
        self.click(self.job_title)
        self.select_dropdown_option(job_title)

    def select_sub_unit(self, sub_unit):
        self.click(self.sub_unit)
        self.select_dropdown_option(sub_unit)

    def click_reset(self):
        self.click(self.reset_button)

    def click_search(self):
        self.click(self.search_button)

    def fill_employee_records_filters(
        self,
        employee_name=None,
        employee_id=None,
        employment_status=None,
        employee_record=None,
        supervisor_name=None,
        job_title=None,
        sub_unit=None,
    ):
        if employee_name:
            self.enter_employee_name(employee_name)
        if employee_id:
            self.enter_employee_id(employee_id)
        if employment_status:
            self.select_employment_status(employment_status)
        if employee_record:
            self.select_employee_record(employee_record)
        if supervisor_name:
            self.enter_supervisor_name(supervisor_name)
        if job_title:
            self.select_job_title(job_title)
        if sub_unit:
            self.select_sub_unit(sub_unit)
        return self

    def search_employee_records(
        self,
        employee_name=None,
        employee_id=None,
        employment_status=None,
        employee_record=None,
        supervisor_name=None,
        job_title=None,
        sub_unit=None,
    ):
        self.fill_employee_records_filters(
            employee_name=employee_name,
            employee_id=employee_id,
            employment_status=employment_status,
            employee_record=employee_record,
            supervisor_name=supervisor_name,
            job_title=job_title,
            sub_unit=sub_unit,
        )
        self.click_search()
        return self

    def get_filter_values(self):
        return {
            "employee_name": self.get_input_value(self.employee_name),
            "employee_id": self.get_input_value(self.employee_id),
            "employment_status": self.get_dropdown_value(self.employment_status_value),
            "employee_record": self.get_dropdown_value(self.employee_record_value),
            "supervisor_name": self.get_input_value(self.supervisor_name),
            "job_title": self.get_dropdown_value(self.job_title_value),
            "sub_unit": self.get_dropdown_value(self.sub_unit_value),
        }

    def validate_reset_employee_records(self, expected_dropdown_values=None):
        filter_values = self.get_filter_values()

        assert filter_values["employee_name"] == "", "Employee Name field was not cleared after reset"
        assert filter_values["employee_id"] == "", "Employee Id field was not cleared after reset"
        assert filter_values["supervisor_name"] == "", "Supervisor Name field was not cleared after reset"

        dropdown_defaults = dict(self.DEFAULT_DROPDOWN_VALUES)
        if expected_dropdown_values:
            dropdown_defaults.update(expected_dropdown_values)

        for field_name, expected_value in dropdown_defaults.items():
            actual_value = filter_values[field_name]
            assert actual_value == expected_value, (
                f"{field_name} was not reset. Expected '{expected_value}', got '{actual_value}'"
            )

        if expected_dropdown_values and "employee_record" in expected_dropdown_values:
            assert filter_values["employee_record"] == expected_dropdown_values["employee_record"], (
                "Employee record filter was not reset to the expected default value"
            )

        return filter_values

    def validate_employee_record(
        self,
        employee_name=None,
        employee_id=None,
        employment_status=None,
        employee_record=None,
        supervisor_name=None,
        job_title=None,
        sub_unit=None,
    ):
        if self.is_visible(self.no_records_found, timeout=3):
            raise AssertionError("Search returned 'No Records Found'")

        expected_values = {
            "employee_name": employee_name,
            "employee_id": str(employee_id).strip() if employee_id is not None else None,
            "employment_status": employment_status,
            "employee_record": employee_record,
            "supervisor_name": supervisor_name,
            "job_title": job_title,
            "sub_unit": sub_unit,
        }

        matching_rows = []
        for row in self.get_all_rows():
            row_data = self.get_row_data(row)
            if self._row_matches_expected(row_data, expected_values):
                matching_rows.append(row_data)

        assert matching_rows, (
            "No table row matched the search filters: "
            f"{ {key: value for key, value in expected_values.items() if value is not None} }"
        )
        return matching_rows[0]

    def reset_employee_records(
        self,
        employee_name=None,
        employee_id=None,
        employment_status=None,
        employee_record=None,
        supervisor_name=None,
        job_title=None,
        sub_unit=None,
        expected_dropdown_values=None,
    ):
        self.fill_employee_records_filters(
            employee_name=employee_name,
            employee_id=employee_id,
            employment_status=employment_status,
            employee_record=employee_record,
            supervisor_name=supervisor_name,
            job_title=job_title,
            sub_unit=sub_unit,
        )
        self.click_reset()
        return self.validate_reset_employee_records(expected_dropdown_values=expected_dropdown_values)

    def search_and_validate_employee_records(
        self,
        employee_name=None,
        employee_id=None,
        employment_status=None,
        employee_record=None,
        supervisor_name=None,
        job_title=None,
        sub_unit=None,
    ):
        self.search_employee_records(
            employee_name=employee_name,
            employee_id=employee_id,
            employment_status=employment_status,
            employee_record=employee_record,
            supervisor_name=supervisor_name,
            job_title=job_title,
            sub_unit=sub_unit,
        )
        return self.validate_employee_record(
            employee_name=employee_name,
            employee_id=employee_id,
            employment_status=employment_status,
            employee_record=employee_record,
            supervisor_name=supervisor_name,
            job_title=job_title,
            sub_unit=sub_unit,
        )
