import requests, os, json, urllib, sys, time
from urllib.parse import quote
from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import SessionNotCreatedException, TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import subprocess
import validators
#from bs4 import BeautifulSoup
import urllib.request
import yt_dlp

app = Flask(__name__)




@app.route('/')
def hello_world():
    return 'Hello from ইয়াসিন'


@app.route('/tera', methods = ['GET', 'POST'])
def get_download_link():
    try:       
        ulink = request.args.get('link')
        print(ulink)
        short_url = ulink
        if not short_url:
            return jsonify({"error": "No URL provided"}), 400

        short_url_id = short_url.split("/")[-1]

        # Step 1: Call the get-info API
        info_api_url = f"https://terabox.hnn.workers.dev/api/get-info?shorturl={short_url_id}&pwd="
        info_response = requests.get(info_api_url)

        if info_response.status_code != 200:
            return jsonify({"error": "Failed to fetch file info", "details": info_response.text}), 500

        info_data = info_response.json()

        if "list" not in info_data:
            return jsonify({"error": "Invalid response structure from get-info API", "details": info_data}), 500

        file_list = info_data.get("list", [])
        if not file_list:
            return jsonify({"error": "No files found in get-info response"}), 404

        # Extract filename and fs_id
        file_info = file_list[0].get("filename")
        fs_id = file_list[0].get("fs_id")
        sign = info_data.get("sign")
        shareid = info_data.get("shareid")
        timestamp = info_data.get("timestamp")
        uk = info_data.get("uk")

        if not all([file_info, fs_id, sign, shareid, timestamp, uk]):
            return jsonify({"error": "Missing essential file information"}), 500

        # Step 2: Call the get-download API
        download_api_url = "https://terabox.hnn.workers.dev/api/get-download"
        download_response = requests.post(download_api_url, json={
            "shareid": shareid,
            "uk": uk,
            "sign": sign,
            "timestamp": timestamp,
            "fs_id": fs_id
        })

        if download_response.status_code != 200:
            return jsonify({"error": "Failed to get download link", "details": download_response.text}), 500

        download_data = download_response.json()

        # Debugging - log the response
        print("get-download API Response:", download_data)

        if "downloadLink" in download_data and "ok" in download_data:
            download_link = download_data.get("downloadLink")
            return jsonify({"download_url": download_link})


        return jsonify({"error": "Invalid response structure from get-download API", "details": download_data}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


  
   


@app.route('/youtube', methods = ['GET'])
def youtube():
    link = request.args.get('link');
    audio = request.args.get('audio');
    video = request.args.get('video');
    print(link, audio, video);
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = options)
    try:
        driver.get("https://en1.savefrom.net/102-youtube-music-downloader-2Ck.html")
        input_field = driver.find_element(By.ID, "sf_url")
        input_field.send_keys('https://youtu.be/6wcfejqYhGk')
        submit_button = driver.find_element(By.ID, "sf_submit")
        submit_button.click()
        wait_time = 10
        nn = 0
        while True:
            try:           
                WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.CLASS_NAME, "media-result")))
                break
            except TimeoutException:
                print('waiting.....')
                driver.save_screenshot(f"/sdcard/screenshot{nn}.png")
                nn += 1
        main_div = driver.find_element(By.CLASS_NAME, "main")
        link_group_divs = main_div.find_elements(By.CLASS_NAME, "link-group")

        # Extract data from the 'a' tags within each 'link-group' div
        data_list = []
        for link_group_div in link_group_divs:
            a_tags = link_group_div.find_elements(By.TAG_NAME, "a")
            for a_tag in a_tags:
                download_attr = a_tag.get_attribute("download")
                quality_attr = a_tag.get_attribute("data-quality")
                type_attr = a_tag.get_attribute("data-type")
                href_attr = a_tag.get_attribute("href")
                data_list.append({
                    "download": download_attr,
                    "data-quality": quality_attr,
                    "data-type": type_attr,
                    "href": href_attr
                })

        print(data_list)
        
        
        driver.save_screenshot("/sdcard/screenshot1.png")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

def update_yt_dlp():
    try:
        # Check current version
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
        current_version = result.stdout.strip()
        print(f"Current yt-dlp version: {current_version}")

        # Get the latest version from PyPI
        result_pypi = subprocess.run(['pip', 'install', '--upgrade', 'yt-dlp'], capture_output=True, text=True)
        if 'Successfully installed' in result_pypi.stdout:
            print(f"yt-dlp updated to the latest version.")
        else:
            print("No updates available for yt-dlp.")

        return True  # Return True if update succeeds

    except Exception as update_error:
        print(f"Update Error: {update_error}")
        return False


@app.route('/allLink', methods = ['GET'])
def allLink():
    print("\n<=====> allLink response <=====>\n")
    ulink = request.args.get('link')
    print(ulink)
    if not ulink:
        return jsonify({"error": "No link provided"}), 400
    # Define a function to capture the download URL
    def get_video_info(url):
        ydl_opts = {
            'format': 'best',  # choose the best quality
            'quiet': True,
            'noplaylist': True,
            'skip_download': True,  # don't download, just get info
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept': '*/*',
                'Connection': 'keep-alive'
            }
        }       
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return info['url']  # returns direct download URL
    try:
        # Fetch download link using yt-dlp
        update_yt_dlp()
        download_url = get_video_info(ulink)
        print(download_url)
        print("\n<=====> allLink finish <=====>\n")
        return jsonify({"download_url": download_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/sing', methods = ['GET'])
def sing():
    print("\n<=====> sing response <=====>\n")
    ulink = request.args.get('link')
    if not ulink:
        return jsonify({"error": "No link provided"}), 400
    def get_specific_audio_link(url):        
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,          
            'dump_single_json': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        audio_links = {f['url'] for f in formats if f['vcodec'] == 'none'}
        print(audio_links)
        for link in audio_links:
            if link.startswith("https://rr"):
                return link
        return None
    try:       
        audio_link = get_specific_audio_link(ulink)       
        if audio_link:
            print("Filtered Audio Link:", audio_link)            
            print("\n<=====> sing finish <=====>\n")
            return jsonify({"download_url": audio_link})
        else:
            print("No matching audio link found.")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)
    

