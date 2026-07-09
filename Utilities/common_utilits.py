from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def webdriver_wait(driver, element, timeout=10):
    WebDriverWait(driver=driver, timeout=timeout).until(
        EC.visibility_of_element_located(element)
    )


def webdriver_wait_url(driver, timeout=10, previous_url=None):
    current_url = previous_url or driver.current_url
    WebDriverWait(driver=driver, timeout=timeout).until(
        EC.url_changes(current_url)
    )

