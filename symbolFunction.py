import time
import pandas as pd
import datetime
import undetected_chromedriver as uc
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import plotly.graph_objects as go


# Function that scrapes Security and its URL
def scrape_urls(driver):    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ReuseTable_PR__IANlW"))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table_rows = soup.find_all('td', class_='ReuseTable_PR__IANlW')
    company_data = {}  
    for row in table_rows:
        link = row.find('a', href=True)
        if link:
            url = link['href']
            company_name = link.text
            company_data[company_name] = url 

    return company_data

def scroll_to_bottom(driver):
    # Function to scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Adjust the sleep duration as needed
    
def is_section_fully_loaded(driver, section_xpath):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, section_xpath))
        )
        return True
    except TimeoutException:
        return False

def main():
    driver = Chrome(headless=False, use_subprocess=True)
    driver.get('https://www.moneycontrol.com/stocks/marketstats/nsehigh/index.php')
    driver.maximize_window()
    # Wait for the specified section to be fully loaded
    section_xpath = '//*[@id="__next"]/main/section/div[2]/section[1]'
    if is_section_fully_loaded(driver, section_xpath):
        print("Section is fully loaded.")
    else:
        print("Section is not fully loaded.")
    
    driver.close()

if __name__ == '__main__':
    main()