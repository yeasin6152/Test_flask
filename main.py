from selenium import webdriver
from flask import Flask, request
from selenium.webdriver.chrome.service import Service
from webdriver_manager_chrome import ChromeDriverManager
from selenium.webdriver.common.by import by

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
    

@app.route('/', method = [ 'GET', 'POST'])
def home():
    if (request.method == 'GET'):
        return download_selenium()



if __name__ == "__main__":
    app.run(debug=True, Port=3000)
