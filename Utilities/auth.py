from Pages.login_page import LoginPage
from Utilities.config import config


def login(driver, username=None, password=None):
    if username is None:
        username = config.Admin_user
    if password is None:
        password = config.Admin_password
    return LoginPage(driver).open_login_page(username=username, password=password)
