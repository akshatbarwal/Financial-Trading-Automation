from bs4 import BeautifulSoup

def scrape_data(driver):
    page_src = driver.page_source
    soup = BeautifulSoup(page_src, 'html.parser')
    table = soup.find('table', class_='frevdat')
    table_data = []
    
    try:
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) == 2:
                key = columns[0].text.strip()
                value = columns[1].text.strip()
                table_data.append([key, value])
    except AttributeError:
        print("No data found on this page. Skipping...")
    
    return table_data