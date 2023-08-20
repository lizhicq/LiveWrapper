from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json,re

def get_html_from_url(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.binary_location = (
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    )

    # Initialize a Chrome webdriver
    driver = webdriver.Chrome(
        executable_path='/Users/lizhicq/Applications/Drivers/chromedriver', 
        options=chrome_options
    )
    # Load the page
    driver.get(url)

    # Get the source HTML of the page
    html = driver.page_source

    # Close the browser
    driver.quit()

    return html

def parse_html_to_json(html):
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all "li1*" divs
    li_elements = soup.find_all('li', id=re.compile('^li1'))
    thunder_set = set()
    for li_element in li_elements:
        input_elements = li_element.find_all('input', type='text')
        for input_element in input_elements:
            value = input_element.get('value')
            if value and value.startswith('thunder://'):
                thunder_set.add(value)
    return thunder_set


if __name__ == "__main__":
    # Get HTML from the URL
    url = 'https://www.kdianying.net/detail-1295.html'
    html = get_html_from_url(url)
    # Parse HTML to JSON
    thunder_json = parse_html_to_json(html)
    for index, value in enumerate(thunder_json):
        print(value, end='\n')
        if (index + 1) % 50 == 0:  # 每50个元素后打印分隔符
            print('\n-----------------------\n')
