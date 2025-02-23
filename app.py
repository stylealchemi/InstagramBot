from flask import Flask, render_template, request
from selenium import webdriver
import chromedriver_autoinstaller
import time

app = Flask(__name__)

# Automatically download ChromeDriver
chromedriver_autoinstaller.install()

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model (required for Render)
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection

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

    # Launch Chrome WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Instagram login
        driver.get("https://www.instagram.com")
        time.sleep(3)

        # Example login steps (update as needed)
        driver.find_element('name', 'username').send_keys(username)
        driver.find_element('name', 'password').send_keys(password)
        driver.find_element('xpath', '//button[@type="submit"]').click()
        time.sleep(5)

        # Send messages to each account
        for account in accounts:
            driver.get(f"https://www.instagram.com/{account.strip()}/")
            time.sleep(3)

            # Send first message
            # (Update to use Instagram's DM system)
            print(f"Sent first message to {account.strip()}")

            # Wait for reply (mocked with sleep)
            time.sleep(20 * 60)  # Wait 20 minutes

            # Send second message
            print(f"Sent second message to {account.strip()}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

    return "Bot finished!"

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def home():
    return render_template('index.html')
