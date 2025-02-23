import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import shutil


def start_automation(data):
    username = data['username']
    password = data['password']
    accounts = data['accounts'].split('\n')
    message1 = data['message1']
    message2 = data['message2']

    # Install ChromeDriver
    chromedriver_autoinstaller.install()

    # Find Chromium executable
    chrome_path = shutil.which("chromium-browser") or shutil.which("google-chrome")

    options = Options()
    options.binary_location = chrome_path  # Use Chromium binary
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(), options=options)

    try:
        driver.get('https://www.instagram.com/accounts/login/')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password, Keys.RETURN)
        WebDriverWait(driver, 10).until(EC.url_contains('/accounts/'))

        for account in accounts:
            driver.get(f'https://www.instagram.com/{account}/')
            time.sleep(random.randint(5, 10))

            message_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Message')]"))
            )
            message_button.click()

            text_area = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'textarea'))
            )
            text_area.send_keys(message1, Keys.RETURN)

            time.sleep(random.randint(1200, 1800))
            text_area.send_keys(message2, Keys.RETURN)

    finally:
        driver.quit()
