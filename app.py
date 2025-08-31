from webdriver_manager.chrome import ChromeDriverManager
import os
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)


def make_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,1696")
    options.binary_location = "/usr/bin/google-chrome"

    # Use webdriver-manager to get the correct chromedriver path
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

@app.get("/scrape")
def scrape():
    driver = make_driver()
    try:
        driver.get("https://example.com/")
        title = driver.title
        # Grab first <h1> text if present
        h1_elems = driver.find_elements(By.TAG_NAME, "h1")
        h1_text = h1_elems[0].text if h1_elems else None
        return jsonify({"url": "https://example.com/", "title": title, "h1": h1_text})
    finally:
        driver.quit()


@app.get("/health")
def health():
    return "ok"


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
