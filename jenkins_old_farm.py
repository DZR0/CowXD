import os
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from tool_shack import wait_for_element, convert_to_int
import logging
import time
import json
import gzip
import requests


########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################
########################################################################################################################################

class JenkinsJr():
    # def __init__(self, browsermob_path)

    percentage_threshhold = 6

    def open_farm():
        logging.info("open_farm()")
        browser = webdriver.Firefox()
        return browser        

    def harvest_field(browser):
        field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "stream-container"))
            )
        try:
            while True:
                element = field.find_element(By.TAG_NAME, "article")
                upvotes_span = element.find_elements(By.CLASS_NAME, "upvote")[1]
                upvotes_count = convert_to_int(upvotes_span.text)
                if upvotes_count > 2000:
                    threshold_percentage = 6
                    like_threshold = int(upvotes_count/100 * threshold_percentage)
                    post_id = element.find_element(By.CLASS_NAME, "badge-evt").get_attribute('href').split('/')[-1]
                    
                    
                    JenkinsJr.get_comments_from_http(browser, post_id, like_threshold)
                browser.execute_script("arguments[0].remove();", element)

        except Exception as e:
            pass

        browser.execute_script("arguments[0].remove();", field)
        

class JenkinsWife():

    def handle_cookie_popup(browser):
        wait_for_element(browser, 'onetrust-group-container', 10)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "onetrust-group-container"))
        )
        cookie_show_options = browser.find_element(By.ID, "onetrust-pc-btn-handler")
        cookie_show_options.click()
        cookie_refuse_all = browser.find_element(By.CLASS_NAME, "ot-pc-refuse-all-handler")
        cookie_refuse_all.click()

    def ask_grandchildren_for_login(browser):
        btn_login = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "visitor-function"))
        )
        time.sleep(1)
        btn_login.click()
        options = browser.find_element(By.CLASS_NAME, "modal")
        btn_use_email = options.find_elements(By.CLASS_NAME, "ui-btn")[4]
        btn_use_email.click()
        username_input = browser.find_element(By.NAME, "username")
        username_input.send_keys("MyGuyOldJenkins")
        username_input = browser.find_element(By.NAME, "password")
        username_input.send_keys(";Xf%#BJUt5VfL%p")
        browser.find_element(By.CLASS_NAME, "login-view__login").click()

    def open_pantry():
        pantry = os.listdir('pantry')
        return pantry
    
    # def place_glass(pantry):
