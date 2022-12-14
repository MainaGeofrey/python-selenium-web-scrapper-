
import itertools
import requests
import json
from bs4 import BeautifulSoup 
import pandas as pd
import os
import csv
import time
import sys
import urllib.request
from datetime import date, datetime
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
import logging
import logging.handlers
import os
import pandas as pd 



 
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", "logs/scrap.log"))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
  #The application will now log all messages with level INFO or above to file
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)



url = 'https://click.weiserstamm.com'

load_dotenv() 
PASSWORD = os.environ.get('PASSWORD')
USERNAME = os.environ.get('USERNAME')


#open browser
def driver_setup():
    try:
        logging.info(datetime.now())
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=chrome_options)
    except Exception as e:
        logging.error("logOpeningBrowserFail:",e)
        logging.info(datetime.now())
    else:
        logging.info("logOpenBrowserSuccess")
        return driver

driver = driver_setup()
def login(driver) :
    try:
        logging.info(datetime.now())
        driver.get("https://click.weiserstamm.com/index.php/site/login")

        input_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'loginform-username')))
        #username.send_keys(os.getenv('username_news'))
        #password.send_keys(os.getenv('password_news'))
        input_element.clear()
        input_element.send_keys(USERNAME)
        
        password_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'loginform-password')))
        password_element.clear()
        password_element.send_keys(PASSWORD)

        driver.find_element(By.XPATH, '//button[@type="submit"]').click()

       # time.sleep(100)
    except Exception as e:
        logging.error("logLogInFail:",e)
        return False
    else:
        logging.info("logLogInSuccess")
        logging.info(datetime.now())
        return True
"""    finally:
        #print("always")
        return """
def csv_writer():
    today = date.today()
    d1 = today.strftime("%d%m%Y")
    name = f'bulk/recipients_{d1}.csv'
    csv_file = open(name, 'w', encoding='utf-8') 
    #writer = csv.writer(csv_file)
    return name
    
def scrap(driver, url):   
    if login(driver):
        try:
           # driver.get("https://click.weiserstamm.com/index.php/outbound")           
            #for i in range(0, last):
            for i in itertools.count(start=1):
                # driver.get(url)
                try:
                    logging.info(datetime.now())
                    logging.info(f"redirect to page {i}")
                    next_url = f"https://click.weiserstamm.com/index.php/outbound/index?page={i}&per-page=1000"
                    driver.get(next_url)
                    #time.sleep(100)
                    
                    
                    df_list = []
                    #t_header = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'th')))
                    t_header = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='w6-container']//th")))
                    columns = [x.text.strip() for x in t_header if len(x.text.strip())> 0]
                    logging.info(columns)
                    #rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
                    rows = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='w6-container']//tr")))

                    for row in rows:
                    #for row in itertools.islice(rows, 10):
                        tds = row.find_elements(By.TAG_NAME, 'td')
                        #tds = row.find_elements(By.XPATH, "//div[@id='w6-container']//td")
                        if len(tds) > 1: #and len(row.text) > 5:
                            #print([x.text.strip() for x in tds if len(x.text) > 0])
                            #logging.info([x.text.strip() for x in tds if len(x.text) > 0])
                            df_list.append(([x.text.strip() for x in tds if len(x.text) > 0]))
                            #logging.info('________________________')
                            
                   # df_list = df_list[0:4]
                    df = pd.DataFrame(df_list, columns = columns)
                    #logging.info(df)
                    
                    try:
                        #file = csv_writer()
                        #logging.info(file)
                        logging.info(datetime.now())
                        df.to_csv('bulk/recipients_11112022.csv', mode='a', encoding='utf-8', index=False)
                    except Exception as e:
                        logging.error("logWriteFileFail:",e)
                        logging.info(datetime.now())
                        return
                    
                    else:
                        logging.info("logWriteFileSuccess")
                    
                    
                except Exception as e:
                    logging.error("logTableScrapFail:",e)
                    return

                else:
                    logging.info("logTableScrapSuccess")
                
                            #next page
            try:

               # time.sleep(100)
                #last = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='pagination']//li[@class='page-item']//a[@class='page-link' and text()='Last']")))
               # last = last.get_attribute("data-page")
                logging.info("last")
               # logging.info(last)
                
                #next = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='pagination']//li[@class='page-item']//a[@class='page-link' and text()='Next']")))
                #next.click()
            except Exception as e:
                logging.error("logNextPageFail:",e)
                
            else:
                logging.info("logNextPageSuccess")
                #return 
            
        except Exception as e:
            logging.error("logScrapFail:",e)
        else:
            logging.info("logScrapSuccess")
            return 

        
scrap(driver, url)
# exit the browser
driver.quit()






