from flask import Flask, request, jsonify, render_template
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_automation():
    data = request.json
    threading.Thread(target=run_bot, args=(data,)).start()
    return jsonify({"message": "Automation started!"})

def run_bot(data):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://www.instagram.com/')
        time.sleep(5)

        # Login
        driver.find_element(By.NAME, 'username').send_keys(data['username'])
        driver.find_element(By.NAME, 'password').send_keys(data['password'], Keys.RETURN)
        time.sleep(10)

        # Send first message
        accounts = data['accounts'].split(',')
        for account in accounts:
            driver.get(f'https://www.instagram.com/{account.strip()}/')
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, 'button[type="button"]').click()
            time.sleep(3)
            driver.find_element(By.TAG_NAME, 'textarea').send_keys(data['message1'], Keys.RETURN)
            time.sleep(10)

        # Wait 20-30 minutes
        time.sleep(60 * 20)

        # Send second message
        for account in accounts:
            driver.get(f'https://www.instagram.com/{account.strip()}/')
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, 'button[type="button"]').click()
            time.sleep(3)
            driver.find_element(By.TAG_NAME, 'textarea').send_keys(data['message2'], Keys.RETURN)
            time.sleep(10)

    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
