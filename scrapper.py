
import requests
import json
from bs4 import BeautifulSoup 
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

"""
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)  """
#driver.get(url)

#login to website
#sign_in_link = driver.find_element_by_link_text('Sign In')
#sign_in_link = driver.find_element(By.LINK_TEXT, "")
#sign_in_link = driver.find_element(By.CLASS_NAME, 'account-menu_login-btn')

#driver function
def driver_setup():
    try:
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
    except Exception as e:
        print("failed log in", e)
        time.sleep(1)
        pass
    else:
        return driver


driver = driver_setup()
def login(driver) :
    try:
        driver.get("https://nation.africa/kenya/account/signin")


        email_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'multiAuthInput')))
        #password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'password')))
        #username.send_keys(os.getenv('username_news'))
        #password.send_keys(os.getenv('password_news'))
        email_element.clear()
        email_element.send_keys('jeffdevops6@gmail.com')


        #driver.find_element_by_xpath("//*[@type='submit']").click()
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        password_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'password')))
        password_element.send_keys('@NemBn!J.rQU3CB')


        #driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        sign_in_link = driver.find_element(By.ID, 'loginRecaptcha')
        #sign_in_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'loginRecaptcha')))
        sign_in_link.click()
       # time.sleep(100)
    except Exception as e:
        print("failed log in", e)
        time.sleep(1)
        pass
    else:
        print("log in success:")

        return True
"""    finally:
        #print("always")
        return """
    
def scrap(driver, url):   
    if login(driver):
        # set csv
        driver.get(url)
            
        today = date.today()
        d1 = today.strftime("%d%m%Y")
        csv_file = open(f'data_news/wsj_articles_{d1}.csv', 'w', encoding='utf-8') 
        writer = csv.writer(csv_file)

        #access all news teasers
        #link_lists = driver.find_elements(By.TAG_NAME, 'section')
        link_lists = driver.find_elements(By.CLASS_NAME, 'teasers-row')
       # link_lists = driver.find_elements(By.XPATH, '//section[@class="teasers-row"][@href]')
        link_lists_total = len(link_lists)
        print("total news is:", link_lists_total)
        
        #collect all link list of latest news
        
        #for i in range(0, link_lists_total):
        for i in driver.find_elements(By.CLASS_NAME, 'teasers-row'):
            article_dict = {}
            
            try:
                link_list = None
                #link_list = WebDriverWait(driver, 10).until(EC.element_located_to_be_selected((By.XPATH, './/h3[@class="teaser-image-large_title title-medium "]')))
                #link_list =driver.find_element(By.CLASS_NAME, 'teaser-image-large').get_attribute('href')
                link_list =i.find_element(By.XPATH, '//a[@class="teaser-image-large"]').get_attribute('href')
                #time.sleep(2)
                #url_w = link_list[i].get_attribute('href')
                article_dict['link'] = link_list
                print(article_dict)
               # link_lists[i].click()
                #driver.get(link_list)
            except Exception as e:
                print("failed scrap", e)
                time.sleep(1)
                pass
            
def soupScrap(driver, url):
    pass

def get_links(url):
    LINKS = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='lxml')
    for html in soup.find_all('section', class_='teasers-row'):
        section = html.find('section')
        link = html.find('a', {"class": "teaser-image-large"}).get('href')
       # link_list =driver.find_element(By.CLASS_NAME, 'teaser-image-large').get_attribute('href')

        print(link)  
        break  
    return LINKS        

scrap(driver, url)
#get_links(url)



