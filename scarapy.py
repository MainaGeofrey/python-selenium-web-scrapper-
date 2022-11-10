import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlencode
import csv
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import datetime
import os

from webdriver_manager.chrome import ChromeDriverManager

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)


url = 'https://www.billboard.com/charts/hot-100/'

#page = requests.get(url)

#print(page.text)

#driver = webdriver.Chrome()
driver.get(url)
src = driver.page_source
print(src)
parser = BeautifulSoup(src, "lxml")
table = parser.find("div", attrs= {"class":"o-chart-results-list-row-container"})
table


#driver.close()