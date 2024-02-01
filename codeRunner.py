from customStratFunction import create_main_dict

# Import the modules
import time
import pandas as pd
import datetime
from pandas.tseries.offsets import BDay
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from prettytable import PrettyTable


def get_dictionary_1():
    # Define the paths and parameters
    excel_file = "moneycontrol/New-52-Week-high-dataLtpGreater20-27-Oct-2023.xlsx"
    today = datetime.datetime.now()
    ndays = datetime.timedelta(days=1)
    date = (today - ndays).date()
    end_date = date.strftime("%Y-%m-%d")
    date_range = pd.date_range(end=end_date, periods=365)
    trading_dates = date_range.date.tolist()
    start_date = trading_dates[0]

    # Create the main dictionary
    main_dict = create_main_dict(excel_file)
    return main_dict

def scrape_urls(driver):    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ReuseTable_PR__p1pXk"))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table_rows = soup.find_all('td', class_='ReuseTable_PR__p1pXk')
    company_data = {}  
    for row in table_rows:
        link = row.find('a', href=True)
        if link:
            url = link['href']
            company_name = link.text
            company_data[company_name] = url 

    return company_data

def get_dictionary_2():
    driver = uc.Chrome(headless=True, use_subprocess=False)
    # Fetch all the URLS for the stocks
    driver.get('https://www.moneycontrol.com/stocks/marketstats/nsehigh/index.php')
    print("Navigating to required page...")
    print('\n')
    time.sleep(2)
    urls_dictionary = scrape_urls(driver)
    print("Scraping URLS...")
    print('\n')
    time.sleep(5)
    driver.quit()
    return urls_dictionary    

def main():
    # dict_1 = get_dictionary_1()
    # time.sleep(2)
    dict_2 = get_dictionary_2()
    time.sleep(2)
    # for keys, vals in dict_1.items():
    #     print(keys,":",vals)
    # time.sleep(1)
    # print("="*50)
    for keys, vals in dict_2.items():
        print(keys,":",vals)
    print("="*50)
    

if __name__ == "__main__":
    main()



