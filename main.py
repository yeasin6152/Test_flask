from selenium import webdriver
from flask import Flask, request
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


app = Flask(__name__)

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
    

@app.route('/')
def home():
    if request.method == 'GET':
        # Handle GET requests
        return "This is a GET request"
    elif request.method == 'POST':
        # Handle POST requests
        return "This is a POST request"

@app.route('/data', methods=['PUT', 'DELETE'])
def handle_data():
    # Handle PUT and DELETE requests for data
    if request.method == 'PUT':
        # ...
    elif request.method == 'DELETE':
        # ...
        



if __name__ == "__main__":
    app.run(debug=True, Port=3000)
