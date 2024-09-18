from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import pandas as pd
import os

# Define function to handle Vercel function call
def handler(event, context):
    # Ensure chromedriver is installed
    chromedriver_autoinstaller.install()

    # Set up headless Chrome with Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    # Set ChromeDriver path
    driver = webdriver.Chrome(options=chrome_options)

    # Google Trends URL
    trends_url = 'https://trends.google.com/trends/trendingsearches/daily'
    driver.get(trends_url)

    # Extract trending data
    trending_items = driver.find_elements_by_css_selector('.details-top .title a')

    # Process extracted data
    trends = []
    for item in trending_items:
        title = item.text
        link = item.get_attribute('href')
        trends.append({'title': title, 'link': link})

    # Store results to a CSV file (in Vercel's temporary /tmp/ directory)
    df = pd.DataFrame(trends)
    csv_path = 'python_app/tmp/google_trends.csv'
    df.to_csv(csv_path, index=False)

    driver.quit()

    # Return result (you can also serve the CSV file)
    return {
        'statusCode': 200,
        'body': {
            'message': 'Scraping completed',
            'csv_path': csv_path
        }
    }
