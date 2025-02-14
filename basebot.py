from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import gunicorn

# Initialize Flask app
app = Flask(__name__)

# Function to send messages using Selenium
def send_messages(username, password, accounts, first_message, reply_message):
    # Start WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")
    time.sleep(5)  # Wait for page to load
    
    # Log in to Instagram
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    username_input.send_keys(username)
    password_input.send_keys(password)
    username_input.send_keys(Keys.RETURN)
    time.sleep(10)  # Wait for login
    
    # Navigate to Instagram Direct Messages
    driver.get("https://www.instagram.com/direct/inbox/")
    time.sleep(5)
    
    # Sending messages to specified accounts
    for account in accounts:
        driver.get(f"https://www.instagram.com/direct/t/{account}/")
        time.sleep(5)
        try:
            text_box = driver.find_element(By.TAG_NAME, "textarea")
            text_box.send_keys(first_message)
            text_box.send_keys(Keys.RETURN)
            print(f"Message sent to {account}")
            time.sleep(random.randint(60, 120))  # Wait 1-2 minutes before sending the next message
        except:
            print(f"Failed to message {account}")
    
    # Check for replies every minute
    replied_accounts = {}
    while True:
        for account in accounts:
            driver.get(f"https://www.instagram.com/direct/t/{account}/")
            time.sleep(5)
            try:
                # Check for a new reply
                messages = driver.find_elements(By.CSS_SELECTOR, "div[role='presentation']")
                if messages and account not in replied_accounts:
                    print(f"Reply detected from {account}")
                    replied_accounts[account] = time.time()  # Store the time of the reply
                
                # If 20 minutes have passed since the reply, send a response
                if account in replied_accounts and time.time() - replied_accounts[account] >= 1200:
                    text_box = driver.find_element(By.TAG_NAME, "textarea")
                    text_box.send_keys(reply_message)
                    text_box.send_keys(Keys.RETURN)
                    print(f"Reply sent to {account} after 20 minutes")
                    del replied_accounts[account]  # Remove from tracking after reply
            except:
                print(f"No reply found from {account}")
        
        time.sleep(60)  # Check every minute for new replies

    # Close WebDriver
    driver.quit()

# Route for the web form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input from the form
        username = request.form['username']
        password = request.form['password']
        accounts = request.form['accounts'].split(',')  # Split accounts by comma
        first_message = request.form['first_message']
        reply_message = request.form['reply_message']
        
        # Run the bot with provided details
        send_messages(username, password, accounts, first_message, reply_message)
        return "Automation Started!"  # Response message
    
    # Render the input form
    return render_template("index.html")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

# HTML Form for User Input (templates/index.html):
# <html>
# <body>
#     <form method="POST">
#         Username: <input type="text" name="username"><br>
#         Password: <input type="password" name="password"><br>
#         Accounts (comma-separated): <input type="text" name="accounts"><br>
#         First Message: <input type="text" name="first_message"><br>
#         Reply Message: <input type="text" name="reply_message"><br>
#         <input type="submit" value="Start Automation">
#     </form>
# </body>
# </html>
