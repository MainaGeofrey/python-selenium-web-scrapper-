
import requests
import json
import bs4
import pandas as pd
import os
import csv
import time
import sys
import urllib.request
from datetime import date
from htmldate import find_date
from dotenv import load_dotenv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from json import JSONDecoder
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service



url = 'https://nation.africa/kenya/news'

#open browser
'''
chrome_options = Options();
chrome_options.add_argument("--window-size=1920,1080");
chrome_options.headless = True
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
ua = UserAgent()
userAgent = ua.random
chrome_options.add_argument(f'user-agent={userAgent}')
#driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
#s = Service( webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options))
#s=Service(ChromeDriverManager().install(), options=chrome_options) '''
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
#driver.get(url)

#login to website
#sign_in_link = driver.find_element_by_link_text('Sign In')
#sign_in_link = driver.find_element(By.LINK_TEXT, "")
#sign_in_link = driver.find_element(By.CLASS_NAME, 'account-menu_login-btn')

#sign_in_link.click()
def login() :
    try:
        driver.get("https://nation.africa/kenya/account/signin")


        email_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'multiAuthInput')))
        #password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password')))
        #username.send_keys(os.getenv('username_news'))
        #password.send_keys(os.getenv('password_news'))
        email_element.clear()
        email_element.send_keys('')


        #driver.find_element_by_xpath("//*[@type='submit']").click()
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        password_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'password')))
        password_element.send_keys('')


        #driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        sign_in_link = driver.find_element(By.ID, 'loginRecaptcha')
        #sign_in_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'loginRecaptcha')))
        sign_in_link.click()
    except Exception as e:
        print("failed log in", e)
        pass
    else:
        print("log in success:")

"""    finally:
        #print("always")
        return """

def scrap():
    if login():
        driver.get(url)
        #time.sleep(100)
        # set csv
        today = date.today()
        d1 = today.strftime("%d%m%Y")
        csv_file = open(f'data_news/wsj_articles_{d1}.csv', 'w', encoding='utf-8') 
        writer = csv.writer(csv_file)

        #access all news teasers
        link_lists = driver.find_elements(By.CLASS_NAME, 'teasers-row')
        time.sleep(1)
        link_lists_total = len(link_lists)
        print("total news is:", link_lists_total)
        
        #collect all link list of latest news
        
        for i in range(0, link_lists_total):
            article_dict = {}
            
            try:
                
                link_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
            except Exception as e:
                print("failed scrap", e)
                time.sleep(1)
                pass
            
        


scrap()


