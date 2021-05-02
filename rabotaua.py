from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import datetime

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome() #options=chrome_options
driver.get('https://rabota.ua/zapros/data-analyst/')
timeout = 10
element_present = EC.presence_of_element_located((By.CLASS_NAME, 'f-vacancylist-top-wrapper'))
WebDriverWait(driver, timeout).until(element_present)


# Получение наибольшей страницы
pagination =  driver.find_element(By.ID, 'ctl00_content_vacancyList_gridList_ctl43_pagerInnerTable')
pages = pagination.text.split('\n')
pages = [x for x in pages if x.isdigit()]
max_page = max(pages)
#


# Получение всех сылок
links_vacs = []
links_len = len(links_vacs)
elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    if "company" in str(elem.get_attribute("href")) and "vacancy" in str(elem.get_attribute("href")) and "recom_score" not in str(elem.get_attribute("href")):
        links_vacs.append(elem.get_attribute("href"))


for page in range(2, int(max_page)+1):
    zapyt = f"https://rabota.ua/zapros/data-analyst/pg{page}"
    driver.get(zapyt)
    timeout = 10
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'f-vacancylist-top-wrapper'))
    WebDriverWait(driver, timeout).until(element_present)
    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        if "company" in str(elem.get_attribute("href")) and "vacancy" in str(elem.get_attribute("href")) and "recom_score" not in str(elem.get_attribute("href")):
            links_vacs.append(elem.get_attribute("href"))
    time.sleep(random.randint(0, 5))
#

# Парсинг текста с сылок
from base_editor import *
count = 1
for link in links_vacs:
    driver.get(link)
    timeout = 10
    element_present = EC.presence_of_element_located((By.ID, "description-wrap"))
    WebDriverWait(driver, timeout).until(element_present)
    desc = driver.find_element(By.ID, "description-wrap")
    fill_base('base_da.txt', desc.text, link=link)
    print(link)
    # drop_dupl_base('base_da.txt')
    print(f'Добавил в базу описание c ссылки {link}')
    print(f"Спарсено {count}/{links_len}")
    time.sleep(random.randint(0, 5))
    count += 1



