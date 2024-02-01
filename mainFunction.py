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

from tableFunction import scrape_data   
from swotFunction import scrape_swot_data

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

    
def main():
    driver = uc.Chrome(headless=False, use_subprocess=False)
    driver.get('https://www.moneycontrol.com/')
    driver.maximize_window()
    # Wait for the element to appear
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "userlink"))
        )
        # If the element is found, it means you have successfully logged in
        print("Successfully logged in!")
        print("\n")
    except Exception as e:
        # If the element is not found within the specified time, you can handle the error or print a message
        print("Login not successful:", e)
        print("\n")

    time.sleep(2)
    
    # Fetch all the URLS for the stocks
    print("Navigating to required page...")
    print('\n')
    driver.get('https://www.moneycontrol.com/stocks/marketstats/nsehigh/index.php')
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    print("Scraping URLS...")
    print('\n')
    urls_dictionary = scrape_urls(driver)
    time.sleep(5)
    # print_dictionary(urls_dictionary)
    # time.sleep(1)

    # Iterate through the dictionary, take one key-value pair at once and run the url through the scrape_swot_data and scrape_data functions. Create a new dictionary with the company name as the key and the value this time will be the data fetched from the two functions.
    # urls_dictionary = dict(list(urls_dictionary.items())[:1])
    company_data = {}
    results = []
    print("Scraping Tables...")
    print('\n')
    for stock, url in urls_dictionary.items():
        driver.get(url)
        swot_data = scrape_swot_data(driver)
        time.sleep(2)
        swot_df = pd.DataFrame(swot_data, columns=['Scores','Description'])
        metrics = ["Strengths", "Weaknesses", "Opportunities", "Threats"]
        swot_df.insert(0, "Metrics", metrics)
        time.sleep(2)
        table_data = scrape_data(driver)
        time.sleep(2)
        table_df = pd.DataFrame(table_data, columns=['Key','Value'])
        time.sleep(1)
        company_data[stock] = {'SWOT_Data': swot_df, 'Table_Data': table_df}
        time.sleep(2)
    
    # Printing the data
    combined_data = []  # List to store data for all stocks

    for stock, data in company_data.items():
        swot_df = data['SWOT_Data']
        table_df = data['Table_Data']
        
        # Check if the keys exist in the table data DataFrame
        if 'Revenue' in table_df['Key'].values:
            revenue = table_df[table_df['Key'] == 'Revenue']['Value'].values[0]
        if 'NetProfit' in table_df['Key'].values:
            net_profit = table_df[table_df['Key'] == 'NetProfit']['Value'].values[0]
        if 'OperatingProfit' in table_df['Key'].values:
            operating_profit = table_df[table_df['Key'] == 'OperatingProfit']['Value'].values[0]
        
        # Combine SWOT and table data for each stock
        combined_data.append({
            'Company': stock,
            'Strengths': swot_df[swot_df['Metrics'] == 'Strengths']['Scores'].values[0],
            'Weaknesses': swot_df[swot_df['Metrics'] == 'Weaknesses']['Scores'].values[0],
            'Opportunities': swot_df[swot_df['Metrics'] == 'Opportunities']['Scores'].values[0],
            'Threats': swot_df[swot_df['Metrics'] == 'Threats']['Scores'].values[0],
            'Revenue': revenue,
            'NetProfit': net_profit,
            'OperatingProfit': operating_profit,
        })

    # Create a DataFrame from the combined data
    combined_df = pd.DataFrame(combined_data)

    # Print the combined DataFrame
    combined_df.to_excel('moneycontrol.xlsx', index = False)

    time.sleep(1)
    print("Closing Driver...")
    print('\n')
    driver.quit()
        

if __name__ == '__main__':
    main()
    
    

