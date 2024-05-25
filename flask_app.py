from flask import Flask, request
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json



app = Flask(__name__)


@app.route('/download_data')
def download_data():
    data = download_selenium()  # Call the download_selenium function
    response_body = json.dumps(data).encode('utf-8')  # Convert data to JSON

    return response_body, 200, {'Content-Type': 'application/json'}  # Return data, status, and headers


def download_selenium():
    chrome_option = webdriver.ChromeOption()
    chrome_option.add_argument("--headless")
    chrome_option.add_argument("--no-sandbox")
    chrome_option.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chome(service=Service(ChromeDriverManager().install()), option=chrome_option)
    driver.get("https://google.com")
    title = driver.title
    language=driver.find_element(By.XPATH, "//div[@id='SIvCob']").text
    data = { 'page title': title, 'language': language}
    return data
