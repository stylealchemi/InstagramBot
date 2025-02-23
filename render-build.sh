#!/usr/bin/env bash

# Update package lists and install dependencies
apt-get update && apt-get install -y wget unzip

# Install Google Chrome
wget -q -O chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./chrome.deb
rm chrome.deb

# Install ChromeDriver
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -q "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/
rm chromedriver_linux64.zip
