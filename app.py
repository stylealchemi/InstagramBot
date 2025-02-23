from flask import Flask, render_template, request, jsonify
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


app = Flask(__name__)

def start_bot(username, password, accounts, message1, message2):
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    # Login
    user_input = driver.find_element(By.NAME, "username")
    pass_input = driver.find_element(By.NAME, "password")
    user_input.send_keys(username)
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.RETURN)
    time.sleep(5)

    for account in accounts:
        driver.get(f"https://www.instagram.com/direct/t/{account}/")
        time.sleep(3)

        try:
            message_box = driver.find_element(By.XPATH, "//textarea")
            message_box.send_keys(message1)
            message_box.send_keys(Keys.RETURN)
            time.sleep(5)

            # Wait for a reply
            replied = False
            start_time = time.time()
            while time.time() - start_time < 1800:  # Check for 30 minutes
                try:
                    latest_message = driver.find_elements(By.XPATH, "//div[contains(@class, 'message')]")[-1]
                    if latest_message.text != message1:
                        replied = True
                        break
                except:
                    pass
                time.sleep(10)  # Check every 10 seconds

            if replied:
                time.sleep(1200)  # Wait an additional 20 minutes before replying
                message_box.send_keys(message2)
                message_box.send_keys(Keys.RETURN)
                time.sleep(5)
        except Exception as e:
            print(f"Error messaging {account}: {e}")
    
    driver.quit()

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    threading.Thread(target=start_bot, args=(
        data['username'], data['password'], data['accounts'],
        data['message1'], data['message2'])).start()
    return jsonify({"message": "Bot started successfully!"})

@app.route('/')
def home():
    return render_template('index.html')  # This serves the frontend page

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    threading.Thread(target=start_bot, args=(
        data['username'], data['password'], data['accounts'],
        data['message1'], data['message2'])).start()
    return jsonify({"message": "Bot started successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def home():
    return render_template('index.html')
