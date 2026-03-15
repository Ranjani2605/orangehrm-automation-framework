import logging

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from Pages.PIM_PAGE.PIM_BASE_PAGE import PIMBasePage
from Pages.base_page import BasePage


class BreadcrumbHelper(BasePage):
    logger = logging.getLogger(__name__)

    breadcrumb_last = (By.CSS_SELECTOR, ".oxd-breadcrumb li:last-child")
    active_tab = (By.CSS_SELECTOR, ".oxd-topbar-body-nav-tab-item.--active")
    header_candidates = [(By.CSS_SELECTOR, ".oxd-topbar-header-title h6"),
                         (By.CSS_SELECTOR, ".oxd-topbar-header-breadcrumb h6"),
                         (By.XPATH, "//h6"),
                        ]


    def get_header_text(self):
        for locator in self.header_candidates:
            if self.is_visible(locator):
                text = self.get_text(locator)
                if text:
                    return text
        raise AssertionError("No visible header found to compare with breadcrumb.")

    def assert_breadcrumb_matches_header(self):
        header_text = self.get_header_text()
        if not self.is_visible(self.breadcrumb_last):
            self.logger.info("Breadcrumb not visible; skipping breadcrumb/header match.")
            return self
        breadcrumb_text = self.get_text(self.breadcrumb_last)
        assert breadcrumb_text == header_text, (
            f"Breadcrumb '{breadcrumb_text}' did not match header '{header_text}'"
        )
        return self

    def verify_tab_bar_text(self, expected_tab_bar):
        try:
            self.logger.info("Verifying tab bar text. Expected: %s", expected_tab_bar)
            if isinstance(expected_tab_bar, tuple):
                tab_bar = expected_tab_bar
                expected_text = None
            else:
                expected_text = expected_tab_bar
                tab_bar = (By.XPATH, f"//a[contains(@class,'oxd-topbar-body-nav-tab-item') and normalize-space()='{expected_text}']")

            assert self.is_visible(tab_bar), f"Tab '{expected_tab_bar}' is not visible."
            actual_text = self.get_text(tab_bar)
            if expected_text is not None:
                assert actual_text == expected_text, f"expected '{expected_text}', but got '{actual_text}'"
            return self
        except Exception as e:
            self.logger.error(f"verify_tab_bar failed: {e}")
            raise


