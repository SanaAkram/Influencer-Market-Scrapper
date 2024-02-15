import json, re, csv, os, time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.common import NoSuchElementException, TimeoutException
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

current_day = str(datetime.now().date()).replace('-', '_')

# Files
all_data_file = f'files/all_data{current_day}.csv'
all_active_campaigns_file = f'files/active_campaigns{current_day}.csv'
all_statuses_file = f'files/all_status_history_{current_day}.csv'

# Define constants
API_KEY = '5hsgwrgeyym1c9hj0fkmd8xggh4h'
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ3X2lkIjoiNDc2MTA4OTItNzdiZC00MGIxLThjODAtZjlkMTJjNzMwZTYyIiwiaWF0IjoxNjk2ODQ3OTQ2fQ.TuiksVtdLFZeKqzCliej0QZpsTQEaMRiKg4rnp88gxI"

Count_HEADERS = {
    'Content-Type': 'application/json',
    'X-Org-Auth': AUTH_TOKEN,
}

Summary_Headers = {
    'Content-Type': 'application/json',
}

OPP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'Content-Type': 'application/json',
}

influencer_url = "https://www.thehandbook.com/celebrity-finder/?advanced=1&celeb_type%5B0%5D=80620&sort=reach"
CAMPAIGNS_ENDPOINT = f'campaign/list?limit=200&key={API_KEY}'
COUNT_ENDPOINT = 'analytics/campaign/count'
STATUS_ENDPOINT = 'campaign/get/status'
leads_endpoint = 'lead/get'
login_url = 'https://marketer.modash.io/login/marketer?redirect=%2Fdiscovery%2Finstagram'
campaign_url = 'https://app.instantly.ai/app/campaign/'

all_leads = []
all_campaigns = []
leads_status = []

# Login
# driver_path = './chromedriver.exe'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    # Add any other headers you need
}

# Chrome Setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-blink-features=InterestCohortAPI")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
# chrome_options.add_argument("--headless")
chrome_options.add_argument(f"user-agent={headers['User-Agent']}")

# Install ChromeDriver and use it
driver_path = ChromeDriverManager().install()
service = Service(executable_path=driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
print('######################     Trying to Log In .....     ###########################')
driver.get(login_url)
username_field = driver.find_element(By.NAME, "email")  # Replace with the correct name attribute
password_field = driver.find_element(By.NAME, "password")  # Replace with the correct name attribute
username_field.send_keys("bilal@segnify.com")
password_field.send_keys("ALHAMDULILLAH786@")
login_button = driver.find_element(By.CLASS_NAME, "_btn_auth_sgbk7_333")
wait1 = WebDriverWait(driver, 11360)
login_button.click()
wait = WebDriverWait(driver, 360)
wait3 = WebDriverWait(driver, 3)
print('######################     Logged In Successfully     ###########################')


def get_influencer_data(url=None):
    email_dropdown = None
    # driver.get(url)
    time.sleep(5.5)
    contact_elements = driver.find_elements(By.CLASS_NAME, '_genericFilterBox_c8zr3_181')[2]
    contact_elements.click()
    li_elements = driver.find_elements(By.CSS_SELECTOR, "ul._selections_c7jz6_127 > li")

    # Print the text content of each <li> element
    for li_element in li_elements:
        if li_element.text == "Has email":
            print(li_element.text, 'Filter has been selected !')
            li_element.click()
            break

    show_influencer = driver.find_element(By.XPATH,
                                          '//*[@id="mainContent"]/div/div[2]/div[2]/div/div[3]/div/div/div[2]/div[2]/div/div/button')
    show_influencer.click()


try:
    data = get_influencer_data(url=influencer_url)
    print(f'Data is {data}')
except Exception as e:
    print(f"Error occured as {e}")
print('Done !')
