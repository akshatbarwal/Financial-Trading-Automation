import time
import pandas as pd
import datetime
import undetected_chromedriver as uc
from Screenshot import Screenshot
from Screenshot import Screenshot_Clipping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO



def main():
    driver = uc.Chrome(headless=False, use_subprocess=False)
    driver.maximize_window()

    # Navigate to the webpage
    driver.get('https://www.moneycontrol.com/stocks/marketstats/nsehigh/index.php')
    ss = Screenshot_clipping.Screenshot()
    img = ss.full_screenshot(driver,save_path=r'.', image_name="Screenshot1.png",is_load_at_runtime=True,load_wait_time=3)
    driver.close()
    driver.quit()

        
if __name__ == '__main__':
    main()