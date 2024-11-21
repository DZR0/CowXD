from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


def wait_for_element(driver, element_locator, timeout=10):
    try:
        if not isinstance(element_locator, tuple):
            raise ValueError("element_locator should be a tuple (locator_type, locator_value)")

        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(element_locator)
        )
    except TimeoutException:
        print(f"Element not found using locators: {element_locator}")
        return None
    except ValueError as ve:
        print(f"Invalid element locator format: {ve}")
        return None
  
def convert_to_int(num_str):
    num_str = num_str.lower().strip()  
    
    if num_str.isdigit():
        return int(num_str)
    
    multiplier = 1
    if 'k' in num_str:
        num_str = num_str.replace('k', '')
        multiplier = 1000
    
    try:
        return int(float(num_str) * multiplier)
    except ValueError:
        return 0