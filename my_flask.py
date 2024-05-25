import requests, os, json, urllib, sys
from urllib.parse import quote
from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import SessionNotCreatedException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello from Flask'

def find_and_extract_hrefs(url, wait_time, data):
  options = webdriver.ChromeOptions()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  options.add_argument("--headless=new")
  driver = webdriver.Chrome(options=options)
  try:
    driver.get(url)
    wait = WebDriverWait(driver, wait_time)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "p-5")))
    # Wait for the div with class "p-5"
    #driver.implicitly_wait(0.5)
    anchor_elements = driver.find_elements(By.CSS_SELECTOR, "a[rel='noopener noreferrer'][href]")
    if anchor_elements:
      print("Found anchor elements:")
      for element in anchor_elements:
        href_link = element.get_attribute("href")
        if not "play.google.com" in href_link:                
          data.append(href_link);           
          #json_data = {"data": data}
          #json_string = json.dumps(json_data, indent=4)
          return data
    else:
      print("No anchor elements found with rel='noopener noreferrer' and href attribute.")
  except TimeoutException:
    print(f"Element (.p-5) not found within {wait_time} seconds.")
  except Exception as e:
    print("An error occurred:", e)

  finally:
    driver.quit();
    


@app.route('/tera/dll', methods = ['GET', 'POST'])
def download():
  ulink = request.args.get('link')
  print(ulink)
  data = []
  ses = requests.Session()
  headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://ytshorts.savetube.me',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  }

  json_data = {
    'url': ulink,
  }
  #resp = ses.post('https://ytshorts.savetube.me/api/v1/terabox-downloader',headers = headers,json = json_data).json()["response"]
  resp = ses.post('https://ytshorts.savetube.me/api/v1/terabox-downloader', headers = headers, json = json_data)

  # Check for successful response status code (e.g., 200)
  if resp.status_code == 200:
    try:
      # Attempt to parse JSON
      resp_ = resp.json()["response"]
      for key in resp_data:
        print(f"> TITLE : {
          key['title']}")
        print("-----------------------------------")
        videos = key['resolutions']
        data.append(videos['HD Video'])
    except JSONDecodeError:
      # Handle JSON parsing error
      print("-----------------------------------")
      #return jsonify({"message": "Invalid response from TeraBox downloader"}), 500

  
  target_url = "https://teradownloader.com/download?link=" + ulink # Replace with your actual URL
  wait_time = 15
  json_string = find_and_extract_hrefs(target_url, wait_time, data)
  # Print or use the JSON string as needed
  if json_string:
    print(json_string);
    print("-----------------------------------")
    return jsonify({
      "data": json_string
    })
  else :
    return jsonify({
      "message": "No links found"
    }), 404 # Return a 404 Not Found status code if no links are found
def remove_brackets_quotes(text):
  chars_to_remove = set('[]')
  return ''.join(char for char in text if char not in chars_to_remove)



if __name__ == '__main__':
  app.run(host = '0.0.0.0', port = 5001, debug = True)
