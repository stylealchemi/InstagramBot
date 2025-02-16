from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import random
import os

app = Flask(__name__)

class InstagramDM:
    def __init__(self, username, password, reply_messages):
        self.username = username
        self.password = password
        self.reply_messages = reply_messages  # Predefined replies

        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        
        self.browser = webdriver.Chrome(options=options)
        
    def login(self):
        """Logs into Instagram using the provided username and password."""
        self.browser.get("https://www.instagram.com/accounts/login")
        time.sleep(3)

        username_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_input = self.browser.find_element(By.NAME, "password")
        
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        
        time.sleep(5)

    def send_message(self, recipient_username, message):
        """Sends a message to the specified recipient."""
        self.browser.get(f"https://www.instagram.com/direct/new/")
        time.sleep(3)

        search_box = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "queryBox"))
        )
        search_box.send_keys(recipient_username)
        time.sleep(3)

        user = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), '{}')]".format(recipient_username)))
        )
        user.click()

        next_button = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Next']"))
        )
        next_button.click()
        time.sleep(3)

        message_box = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        time.sleep(3)

    def check_and_reply(self, recipient_username):
        """Checks for new messages from the recipient and replies with a predefined message."""
        self.browser.get("https://www.instagram.com/direct/inbox/")
        time.sleep(5)
        
        try:
            conversation = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{recipient_username}')]"))
            )
            conversation.click()
            time.sleep(3)
            
            messages = self.browser.find_elements(By.CSS_SELECTOR, "div[role='listitem']")
            if messages:
                last_message = messages[-1].text.lower()
                if last_message and recipient_username not in last_message:
                    delay = random.randint(1200, 1800)  # Random delay between 20 and 30 minutes
                    time.sleep(delay)
                    
                    reply_message = random.choice(self.reply_messages)  # Choose a predefined reply
                    message_box = WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "textarea"))
                    )
                    message_box.send_keys(reply_message)
                    message_box.send_keys(Keys.ENTER)
                    time.sleep(3)
        except:
            pass

    def close_browser(self):
        """Closes the browser session."""
        self.browser.quit()

# Flask Routes for Render.com Integration
@app.route("/send_message", methods=["POST"])
def send_message_api():
    data = request.json
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    recipient = data.get("recipient")
    message = data.get("message")
    reply_messages = ["Thanks for your reply! 😊", "I appreciate your message!", "Great to hear from you!"]
    
    bot = InstagramDM(username, password, reply_messages)
    bot.login()
    bot.send_message(recipient, message)
    bot.close_browser()
    
    return jsonify({"status": "Message sent successfully"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render.com auto-assigns a port
    app.run(host="0.0.0.0", port=port)
