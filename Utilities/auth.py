import os

from pages.login_page.login_page import LoginPage
from Utilities.config_reader import Config


def login(driver, username=None, password=None):
    username = username or os.getenv("ORANGEHRM_USERNAME") or Config.USERNAME
    password = password or os.getenv("ORANGEHRM_PASSWORD") or Config.PASSWORD
    return LoginPage(driver).open_login_page(username=username, password=password)


def logout(driver):
    return LoginPage(driver).logout_page()
