from bs4 import BeautifulSoup

def scrape_swot_data(driver):
    page_src = driver.page_source
    soup = BeautifulSoup(page_src, 'html.parser')
    # Initialize lists to store the extracted data
    scores = []
    descriptions = []

    try:
        # Find all <li> elements with class "swotliClass"
        swot_items = soup.find_all('li', class_='swotliClass')

        # Extract data from each <li> element
        for swot_item in swot_items:
            a_tag = swot_item.find('a')
            if a_tag:
                score = a_tag.find('strong').text.strip().split('(')[1].replace(')', '')
                description = a_tag.find('em').text.strip()

                # Append the extracted data to the lists
                scores.append(int(score))
                descriptions.append(description)
    except AttributeError:
        print("No SWOT data found on this page. Skipping...")

    # Create a DataFrame
    data = {'Scores': scores, 'Description': descriptions}
    return data