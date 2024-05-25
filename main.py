"""from selenium import webdriver
from flask import Flask, request
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


app = Flask(__name__)
async def app(scope, receive, send):
    # Set the response status and headers
    await send({
        'type': 'http.response.start',
        'status': 200,  # Change this to the appropriate status code
        'headers': [
            (b'content-type', b'text/plain'),  # Example header
        ],
    })

    # Optionally, send response body
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',  # Example response body
    })


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





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)  # Change host and port as needed
"""
import uvicorn
from flask_app import app  # Import your Flask application
async def app(scope, receive, send):
    # Set the response status and headers
    await send({
        'type': 'http.response.start',
        'status': 200,  # Change this to the appropriate status code
        'headers': [
            (b'content-type', b'text/plain'),  # Example header
        ],
    })

    # Optionally, send response body
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',  # Example response body
    })
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
