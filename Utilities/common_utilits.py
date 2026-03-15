from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import *




def webdriver_wait(driver, element):
    WebDriverWait(driver=driver, timeout=10).until(EC.visibility_of_element_located((element)))



def webdriver_wait(driver, element, timeout):
    WebDriverWait(driver = driver, timeout=timeout).until(EC.visibility_of_element_located((element)))


def webdriver_wait_url(driver, timeout):
    WebDriverWait(driver=driver, timeout=timeout).until(EC.url_changes(containt)





