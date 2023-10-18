from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
WHATSAPP_URL = 'https://web.whatsapp.com/'
TIME_LOAD_BROWSER = 10
CONTACT_NAME = "Gym"

def connect_whatsapp():
    try:
        driver = webdriver.Chrome()
        driver.get(WHATSAPP_URL)
        time.sleep(TIME_LOAD_BROWSER)
        wait_login(driver)
        search_box = driver.find_element(By.XPATH, '//*[contains(@class, "selectable-text copyable-text")]')
        search_box.send_keys(CONTACT_NAME)
        time.sleep(2)  # Wait for search results to load
        chat = driver.find_element(By.XPATH, f"//span[@title='{CONTACT_NAME}']")
        chat.click()
        time.sleep(2)
        return driver
    except WebDriverException as err:
        print(err)
        raise Exception("Invalid URL")
    
def wait_login(driver):
    element = "Use WhatsApp on your computer"
    print(element)
    while element == "Use WhatsApp on your computer":
        try:
            divs = driver.find_elements(By.CSS_SELECTOR, "div[class='landing-window']")
            element = divs[0].text.strip().split("\n")[0]
            if element != "Use WhatsApp on your computer":
                break  # Exit the loop when the element changes
        except:
            print("Element not found or timed out, logging in...")
            break  # Exit the loop on error or timeout
    time.sleep(TIME_LOAD_BROWSER)

driver = connect_whatsapp()

def send_message(message):
    try:
        input_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']")
        time.sleep(2)
        input_box.send_keys(message + Keys.ENTER)
        print("sent: ", message)
    except AttributeError:
        raise Exception("Invalid object could be due to invalid URL")
    
def last_message():
    print("read last")
    last_message = "Do you want to..."
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.message-out")))
    while last_message == "Do you want to...":
        message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
        # Extract the text content of the last message
        last_message = message_elements[-1].text.strip().split("\n")[0]
        if last_message == "Insert new exercise":
            last_message = "What muscle?"
    return last_message

def read_last_message():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.message-out")))
    message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
    last_message = message_elements[-1].text.strip().split("\n")[0]
    return last_message

def wait_refresh(last_message_text):
    return_message = ""
    print("starting refresh")
    message = read_last_message()
    print(f"refresh sees last message as {message}")
    print("waiting to start sess")
    while return_message != "Sess" and return_message != "sess":      
        return_message = read_last_message()
        print(return_message)
    return return_message

def send_and_wait(message, last_message_sent):
    send_message(message)
    returned_message = wait_refresh(last_message_sent)
    # returned_message = last_message(driver)
    return returned_message
