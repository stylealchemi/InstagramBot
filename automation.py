from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random

def start_automation(data):
    username = data['username']
    password = data['password']
    accounts = data['accounts'].split('\n')
    message1 = data['message1']
    message2 = data['message2']

    driver = webdriver.Chrome()
    driver.get('https://www.instagram.com')
    time.sleep(5)

    # Login
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password, Keys.RETURN)
    time.sleep(5)

    # Send messages
    for account in accounts:
        driver.get(f'https://www.instagram.com/{account}/')
        time.sleep(random.randint(5, 10))
        # Code to send message1, wait for reply, and send message2 after 20-30 min
        # Simplified example
        time.sleep(random.randint(1200, 1800))

    driver.quit()
