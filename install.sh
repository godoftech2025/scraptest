#!/usr/bin/env bash
set -e

apt-get update && apt-get install -y wget gnupg curl unzip

# Install Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
  > /etc/apt/sources.list.d/google-chrome.list
apt-get update && apt-get install -y google-chrome-stable

# Install matching ChromeDriver
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d. -f1)
DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}")
curl -Lo /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip"
unzip -o /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Verify chromedriver exists
if [ ! -f /usr/local/bin/chromedriver ]; then
  echo "Chromedriver not found!"
  exit 1
fi
