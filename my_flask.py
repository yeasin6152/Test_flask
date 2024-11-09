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
from bs4 import BeautifulSoup
import urllib.request
import yt_dlp

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from ইয়াসিন'

def find_and_extract_hrefs(url, wait_time, data):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = options)
    try:
        driver.get(url)
        wait = WebDriverWait(driver, wait_time)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "p-5")))
        anchor_elements = driver.find_elements(By.CSS_SELECTOR, "a[rel='noopener noreferrer'][href]")
        if anchor_elements:
            print("Found anchor elements:")
            for element in anchor_elements:
                href_link = element.get_attribute("href")
                if not "play.google.com" in href_link:
                    print("ok")
                    data.append(href_link);
                    #json_data = {"data": data}
                    #json_string = json.dumps(json_data, indent=4)
            return data
        else :
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
                print(f"> TITLE : {key['title']}")
                print("-----------------------------------")
                videos = key['resolutions']
                data.append(videos['HD Video'])
        except Exception as e:
            # Handle JSON parsing error
            print("-----------------------------------")
            #return jsonify({"message": "Invalid response from TeraBox downloader"}), 500


    target_url = "https://teradownloader.com/download?link=" + ulink # Replace with your actual URL
    wait_time = 15
    json_string = find_and_extract_hrefs(target_url, wait_time, data)
    # Print or use the JSON string as needed
    if data:
        print(json_string);
        print("-----------------------------------")
        return jsonify({"data": json_string})
    else :
        return jsonify({"message": "No links found"}), 404 # Return a 404 Not Found status code if no links are found
                
def remove_brackets_quotes(text):
    chars_to_remove = set('[]')
    return ''.join(char for char in text if char not in chars_to_remove)

@app.route('/dalle', methods = ['GET'])
def dalle():
    prompt = request.args.get('prompt');
    print(prompt)
    urls = []
    email = request.args.get('email');
    print(email)
    pass_word = request.args.get('pass');
    print(pass_word)
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = options)
    try:
        driver.get("https://www.bing.com/images/create?")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "create_btn_c")))
        join_btn = driver.find_element(By.ID, "create_btn_c")
        join_btn.click()
        print(1)
        driver.save_screenshot("/sdcard/screenshot.png")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "signin_content")))
            signin_link = driver.find_element(By.XPATH, '//a[@title="Sign in with a personal account"]')
            signin_link.click()
            print(2)
            driver.save_screenshot("/sdcard/screenshot1.png")
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "i0116")))
            userName = driver.find_element(By.ID, "i0116")
            userName.send_keys(email + Keys.ENTER)
            print(3)
            driver.save_screenshot("/sdcard/screenshot2.png")

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "i0118")))
            passWord = driver.find_element(By.ID, "i0118")
            passWord.send_keys(pass_word + Keys.ENTER)
            print(4)
            driver.save_screenshot("/sdcard/screenshot3.png")
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "checkboxField")))
                yes = driver.find_element(By.ID, "checkboxField")
                yes.click()
                print(5)
                driver.save_screenshot("/sdcard/screenshot4.png")
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "acceptButton")))
                yes = driver.find_element(By.ID, "acceptButton")
                yes.click()
                print(6)
                driver.save_screenshot("/sdcard/screenshot5.png")
            except TimeoutException:
                print(f"Element (checkboxField and acceptButton) not found within seconds.")
            except Exception as e:
                print(f"Element (checkboxField and acceptButton) problem")
                print("An error occurred:", e)
        except TimeoutException:
            print(f"Element (title=\"Sign in with a personal account\") not found within seconds.")
        except Exception as e:
            print(f"Element (title=\"Sign in with a personal account\") problem")
            print("An error occurred:", e)

        token_balance_element = driver.find_element(By.ID, 'token_bal')
        token_balance = token_balance_element.text
        print(token_balance)
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.ID, "create_btn_c")))
        input = driver.find_element(By.ID, "create_btn_c")
        input.send_keys(prompt + Keys.ENTER)
        print(7)

        driver.save_screenshot("/sdcard/screenshot6.png")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "gil_n_rc")))
        yes = driver.find_element(By.ID, "gil_n_rc")
        yes.click()
        print(8)

        driver.save_screenshot("/sdcard/screenshot7.png")
        """
        urls = []  # Empty list to store image URLs

    # ... (rest of your code for setting up WebDriver and handling login)

    try:
        # Wait for the creation results element
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "girrcc")))
        creation_results = driver.find_element(By.ID, "girrcc")

        # Check if the title matches the expected prompt
        if creation_results.get_attribute("title") == prompt:
            # Find all image elements within the creation results
            images = creation_results.find_elements(By.TAG_NAME, "img")

            # Extract image URLs from each image element
            for image in images:
                src = image.get_attribute("src")
                if src:  # Ensure URL exists before appending
                    urls.append(src)

        # Handle the case where the title doesn't match
        else:
            print(f"Prompt '{prompt}' not found in creation results.")

    except TimeoutException:
        print(f"Element (ID='girrcc') not found within seconds.")
    except Exception as e:
        WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "img_cont")))
        divs = driver.find_elements(By.CLASS_NAME, "img_cont")
        print(8)
        driver.save_screenshot("/sdcard/screenshot6.png")
        for div in divs:
            img = div.find_element(By.TAG_NAME, "img")
            src = img.get_attribute("src")
            urls.append(src)

        # Add explicit return statement for success case
        if urls:
            return jsonify({"data": urls})
        """
    except TimeoutException:
        print(f"Element (.p-5) not found within seconds.")
    except Exception as e:
        print("An error occurred:", e)

    finally:
        driver.quit()

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
    """
    
    <input type="text" name="sf_url" value="" autofocus="" placeholder="Enter the URL" id="sf_url" onfocus="if(this.value &amp;&amp; this.select){this.select()}">
    
    
    
    
    
    try:
        driver.get("https://y2mate.nu/Pio1/")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, 'url')))
        input_element = driver.find_element(By.ID, 'url')
        input_element.send_keys(link + Keys.ENTER);
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, '//form[@autocomplete="off" and @method="post"]//div[@id="" and @style="justify-content: center;"]'))
        )
        download_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Download"))
        )
        download_url = download_link.get_attribute('href')
        print(download_url)
        if download_url:
            return jsonify({"message": "Please check screenshot image", "href_link": download_url})
        else:
            return jsonify({"message": "Please check screenshot image", "href_link": ""})                                       
    except NoSuchElementException:
        print("Error: Button element not found within the specified timeout.")
    except Exception as e:
        print("An error occurred:", e)
        target_url = ("https://download.y2api.com/api/widgetplus?url=" + link)
        driver.get(target_url)        
        wait = WebDriverWait(driver, 20) # Adjust the timeout as necessary
        try:
            # Wait for the table elements
            td_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[@class='px-4 py-4 text-center']")))
            #driver.save_screenshot("/sdcard/screenshot1.png")
        except TimeoutException as e:
            print(f"Error: Table elements not found within 20 seconds: {e}")
            # Handle the case where the table is not present (optional)
        else :
            button_elements = []
            for td_element in td_elements:
                buttons_found = td_element.find_elements(By.XPATH, ".//button")
                if buttons_found:
                    button_elements.extend(buttons_found)                    
                else :
                    print("No button elements found!")
            if button_elements: # Check if any buttons were found
                # Click the first button
                first_button = button_elements[0]
                first_button.click()
                print(f"Successfully clicked the first button: {first_button.text}")
                try:
                    # Wait for the download progress bar (or alternative indicator)
                    progress_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//progress[@value='100']")))
                    # Or: Use another wait condition for download completion
                    #driver.save_screenshot("/sdcard/screenshot2.png")
                except TimeoutException as e:
                    print(f"Error: Download progress not complete within 20 seconds: {e}")
                else :
                    try:
                        song_info_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='px-4 py-5 sm:p-6']")))
                        time.sleep(10)
                    except TimeoutException as e:
                        print("Error: Song information element not found within 10 seconds:", e)
                    else:
                        # Extract song title (optional)
                        #driver.save_screenshot("/sdcard/screenshot3.png")
                        song_title_element = song_info_element.find_element(By.TAG_NAME, "h1")
                        #print(f"song_title_element: {song_title_element}")
                        song_title = song_title_element.text
                        print(f"Song title: {song_title}")
                        download_link_element = song_info_element.find_element(By.XPATH, ".//a[contains(@class, 'group-hover:from-purple-600')]")
                        download_link = download_link_element.get_attribute('href')
                        print(f"Download link: {download_link}")
                        if download_link:
                            return jsonify({"message": "Please check screenshot image", "href_link": download_link})
                        else:
                            return jsonify({"message": "Please check screenshot image", "href_link": ""})        
    finally:
        driver.quit()
    """
@app.route('/fakechat', methods = ['GET'])
def fakechat():
    name = request.args.get('name');
    print(name) # নাম
    online_Status = request.args.get('online_Status');
    print(online_Status) # Active 1 hour ago
    message_Break = request.args.get('message_Break');
    print(message_Break) # Today 5:13 PM
    header_Visible = request.args.get('header_Visible');
    header_Visible = header_Visible.split()[-1].lower()
    print(header_Visible) # yes or no
    footer_Visible = request.args.get('footer_Visible');
    footer_Visible = footer_Visible.split()[-1].lower()
    print(footer_Visible) # yes or no
    profile_Image = request.args.get('profile_Image');
    print(profile_Image) # link or no
    message_Image = request.args.get('message_Image');
    print(message_Image) # link or no
    profile_Message = request.args.get('profile_Message');
    print(profile_Message) # Amar sonar ,, tuntuni afa
    other_Message = request.args.get('other_Message');
    print(other_Message) # Bangla Ami tomay ,, এই কথা কেনো

    profile_Message_list = list_create(profile_Message)
    other_Message_list = list_create(other_Message)
    print(profile_Message_list)

    message_Image_list = list_create(message_Image);
    print(message_Image_list)
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = options)
    try:
        driver.get("https://zeoob.com/generate-messenger-chat/#google_vignette")
        print(1)
        driver.save_screenshot("/sdcard/screenshot1.png");
        #handle_modal(driver)  # Call the new function
        account_name_input = driver.find_element(By.CSS_SELECTOR, "input.zeoob_form_control.account_name")
        account_name_input.clear()
        account_name_input.send_keys(name)
        print(2)
        driver.save_screenshot("/sdcard/screenshot2.png");

        account_status_input = driver.find_element(By.CSS_SELECTOR, "input.zeoob_form_control.online_status")
        account_status_input.clear()
        account_status_input.send_keys(online_Status)
        print(3)
        driver.save_screenshot("/sdcard/screenshot3.png");
        handle_modal(driver)
        try:
            print("finding coocke close button")
            close_button = driver.find_element(By.CSS_SELECTOR, "button.close.zpt-allow-cookies")
            close_button.click();
        except: # Catch any exception during click (optional)
            print("Error clicking close button (might not be present)")
            print(4)
        driver.save_screenshot("/sdcard/screenshot4.png");
        remove_icon = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='person1_message']//span[@class='glyphicon glyphicon-trash remove_icon delete__btn']")))
        remove_icon.click()
        remove_icon2 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='person2_message']//span[@class='glyphicon glyphicon-trash remove_icon delete__btn']")))
        remove_icon2.click()
        remove_icon3 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='text_break_post']//span[@class='glyphicon glyphicon-trash remove_icon delete__btn']")))
        remove_icon3.click()
        if "no" in header_Visible:
            radio_button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='header_visible']")))
            radio_button.click()


        for i in range(len(profile_Message_list)):
            # Profile Message পাঠানো
            print(profile_Message_list[i]);
            element = driver.find_element(By.ID, "first_tab_btn")
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.ID, "first_tab_btn")))
            element.click()
            #person_one_tab = driver.find_element(By.CSS_SELECTOR, "li#first_tab_btn.presentation.active")
            #person_one_tab.click()
            print("pass1")
            textarea = driver.find_element(By.CSS_SELECTOR, "textarea.zeoob_form_control.zeoob_text_area.person1_textarea")
            textarea.clear()
            textarea.send_keys(profile_Message_list[i])
            print("pass2")
            wait = WebDriverWait(driver, 10)
            send_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.save_btn.send_message_btn.send_message_1")))
            send_button.click()
            print("pass3")
            print(f" {i}")
            driver.save_screenshot(f"/sdcard/screenshot {4+i+1}.png");

            # Other Message পাঠানো
            if i < len(other_Message_list) and other_Message_list[i]:
                person_two_tab = driver.find_element(By.CSS_SELECTOR, "li.presentation:nth-child(2)") # Adjust as needed
                person_two_tab.click()
                print("pass4")
                textarea = driver.find_element(By.CSS_SELECTOR, "textarea.zeoob_form_control.zeoob_text_area.person2_textarea") # Adjust as needed
                textarea.clear()
                print("pass5")
                textarea.send_keys(other_Message_list[i])
                send_button = driver.find_element(By.CSS_SELECTOR, "button.save_btn.send_message_btn.send_message_2") # Adjust as needed
                send_button.click()
                print("pass6")
                print(f" {i}")
                driver.save_screenshot(f"/sdcard/screenshot {10+i+1}.png");
            else :
                print("other_Message text নাই")

        profile_image_url = "https://i.ibb.co.com/mHJrw0x/FB-IMG-1727342593694.jpg" # Replace with your actual image URL
        downloaded_image_path = get_image_path(profile_image_url)
        file_input = driver.find_element(By.CSS_SELECTOR, "input.upload_img_input")
        file_input.send_keys(downloaded_image_path)
        print("pass7")
        driver.save_screenshot("/sdcard/screenshot20.png")
        bb = "no";
        url = "";
        for i in range(len(message_Image_list)):
            url = message_Image_list[i];
            if url.strip() and (url.startswith("http://") or url.startswith("https://")):
                url = url.strip();
            else :
                url = "https://i.ibb.co.com/mHJrw0x/FB-IMG-1727342593694.jpg";
                if bb == "no":
                    print(url)
                    element = driver.find_element(By.ID, "first_tab_btn")
                    wait = WebDriverWait(driver, 10)
                    element = wait.until(EC.element_to_be_clickable((By.ID, "first_tab_btn")))
                    element.click()
                    wait = WebDriverWait(driver, 10) # Change 10 to a suitable timeout in seconds
                    second_div = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'upload_img')))
                    all_divs = driver.find_elements(By.CLASS_NAME, 'hidden')
                    second_div = all_divs[1]
                    downloaded_image_path = get_image_path(url)
                    second_div.send_keys(downloaded_image_path)
                    print("pass8")
                elif bb == 'yes':
                    person_two_tab = driver.find_element(By.CSS_SELECTOR, "li.presentation:nth-child(2)") # Adjust as needed
                    person_two_tab.click()
                    wait = WebDriverWait(driver, 10) # Change 10 to a suitable timeout in seconds
                    second_div = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'upload_img')))
                    all_divs = driver.find_elements(By.CLASS_NAME, 'hidden')
                    second_div = all_divs[1]
                    downloaded_image_path = get_image_path(url)
                    second_div.send_keys(downloaded_image_path)
            bb = 'no';
            print("pass9")
        print("pass10")
        scroll_position = 1400
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        driver.save_screenshot("/sdcard/screenshot20.png")
        wait = WebDriverWait(driver, 10) # Adjust the timeout as needed
        button = wait.until(EC.element_to_be_clickable((By.ID, "renderIm")))
        button.click()
        print("pass11")
        download_button_wait = WebDriverWait(driver, 5) # Adjust timeout as needed
        download_button = download_button_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.save_btn[download]")))

        download_link = download_button.get_attribute("href")
        print(f"Download Link: {download_link}")
        if download_link:
            return jsonify({"message": "Please check screenshot image", "href_link": download_link})

    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit();


def list_create(massage):
    massage_list = '';
    if ',,' in massage:
        massage_list = massage.split(',,')
    else :
        massage_list = [massage];
    return massage_list



def get_image_path(image_url):
    current_dir = os.path.dirname(os.path.abspath(__file__)) # Get script's directory

    # Extract filename from URL
    filename = os.path.basename(image_url)
    # Create a descriptive filename with timestamp (optional)
    timestamp = int(time.time())
    descriptive_filename = f" {current_dir}/ {filename}- {timestamp}.jpg" # Modify extension if needed
    # Download the image using the absolute path
    try:
        urllib.request.urlretrieve(image_url, descriptive_filename)
        print(f"Image downloaded successfully as ' {descriptive_filename}'.")
    except Exception as e:
        print(f"Error downloading image: {e}")

    return descriptive_filename


def handle_modal(driver):
    """Waits for the modal and clicks the Agree button if present."""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "modal-body")))
        try:
            agree_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-agree[data-href='/generate-messenger-chat/']")
            agree_button.click()
            print("Successfully clicked Agree button")
        except: # Catch any exception during click (optional)
            print("Error clicking Agree button (might not be present)")
    except TimeoutException:
        print("Modal not found. Continuing without clicking Agree.");



@app.route('/prompt', methods = ['GET'])
def prompt():
    print("prompt response")
    link = request.args.get('link');
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options = options)
    try:
        driver.get("https://imageprompt.org/image-to-prompt")        
        image_input = driver.find_element(By.ID, 'image-url')
        image_input.send_keys(link)
        driver.save_screenshot("/sdcard/screenshot1.png")
        # Find the "Load Image URL" button and click it
        load_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Load Image URL')]")
        load_button.click()
        driver.save_screenshot("/sdcard/screenshot2.png")
        # Wait for the "Generate Prompt" button to become enabled
        wait = WebDriverWait(driver, 10)
        generate_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Generate Prompt')]")))
        driver.save_screenshot("/sdcard/screenshot3.png")
        # Click the "Generate Prompt" button
        generate_button.click()
        driver.save_screenshot("/sdcard/screenshot20.png")
        textarea = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//textarea[@class='w-full h-36 p-2 border border-gray-300 bg-muted text-muted-forground rounded focus:ring-2 focus:ring-purple-500 resize-none mb-2 pr-10']")))
        driver.save_screenshot("/sdcard/screenshot21.png")
        # Get the text from the textarea
        text = textarea.text

        # Print the retrieved text
        print(text)
        if text:
            return jsonify({"message": text})
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()
    
@app.route('/allLink', methods = ['GET'])
def allLink():
    print("\n<=====> allLink response <=====>\n")
    ulink = request.args.get('link')
    if not ulink:
        return jsonify({"error": "No link provided"}), 400
    # Define a function to capture the download URL
    def get_video_info(url):
        ydl_opts = {
            'format': 'best',  # choose the best quality
            'quiet': True,
            'noplaylist': True,
            'skip_download': True,  # don't download, just get info
        }       
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info['url']  # returns direct download URL
    try:
        # Fetch download link using yt-dlp
        download_url = get_video_info(ulink)
        print(download_url)
        print("\n<=====> allLink finish <=====>\n")
        return jsonify({"download_url": download_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
    

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)

'''


<a role="button" id="create_btn_c" class="gi_btn_p " aria-label="Create" name="Create" data-cd="" tabindex="0" href="javascript:void(0)" h="ID=images,5056.1" type="button"><div id="create_btn_e"></div><img src="/rp/3mmOYqoyp9J3D-7ONwKXgwCd7Lk.svg" id="create_btn_i" aria-label="Create" width="20" height="20" role="img" class="rms_img" data-bm="4"><span id="create_btn" data-sm="Surprise Me" data-ct="Create" data-enabled="Create" data-disabled="Creating" type="submit" aria-label="Create">Create</span></a>

<div id="gil_n_rc"><a class="gil_n_btn gil_n_active" aria-current="True" aria-label="Creations" title="Creations" role="button" href="/images/create/create-an-image-featuring-a-silhouette-of-a-person/1-66c14d90d55547bf94e4ab042b5e2a51?FORM=GLP2CR" h="ID=images,5085.1"><span>Creations</span><div id="gil_n_rc_g" class="gil_n_g"></div></a></div>
<div id="token_bal" aria-label="11 coins available">11</div>
<div id="girrvc">
<div id="girrcc" class="girrcswp"><a class="girr_set girrcswp seled" title="a beautiful lady carrying flowers " data-imgcount="4" role="button" typeof="button" href="/images/create/a-beautiful-lady-carrying-flowers/1-66c27b1b59ee4ecb99be0c26a118e00f?FORM=GUH2CR" h="ID=images,5053.1"><div class="girrgrid girrcswp" data-imgcount="4"><img src="https://th.bing.com/th/id/OIG1.BvVRGHZNKpM8._jjMbwF?w=40&amp;h=40&amp;c=6&amp;o=5&amp;dpr=2.7&amp;pid=ImgGn" alt="a beautiful lady carrying flowers " data-bm="35">
'''