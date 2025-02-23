
import os
from flask import Flask, render_template, request
from selenium import webdriver
import chromedriver_autoinstaller
import time

app = Flask(__name__)

# Automatically download ChromeDriver
chromedriver_autoinstaller.install()

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "/usr/bin/google-chrome"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-bot', methods=['POST'])
def start_bot():
    username = request.form['username']
    password = request.form['password']
    accounts = request.form['accounts'].split(',')
    first_message = request.form['first_message']
    second_message = request.form['second_message']

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.instagram.com")
        time.sleep(3)
        driver.find_element('name', 'username').send_keys(username)
        driver.find_element('name', 'password').send_keys(password)
        driver.find_element('xpath', '//button[@type="submit"]').click()
        time.sleep(5)

        for account in accounts:
            driver.get(f"https://www.instagram.com/{account.strip()}/")
            time.sleep(3)
            print(f"Sent first message to {account.strip()}")
            time.sleep(20 * 60)
            print(f"Sent second message to {account.strip()}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

    return "Bot finished!"

if __name__ == '__main__':
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
