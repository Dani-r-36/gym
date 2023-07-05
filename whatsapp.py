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
    while element == "Use WhatsApp on your computer":
        divs = driver.find_elements(By.CSS_SELECTOR, "div[class='landing-window']")
        if len(divs) == 0:
            break
        element = divs[0].text
        element = element.strip().split("\n")
        element = element[0]
        print(element)
    time.sleep(TIME_LOAD_BROWSER)

driver = connect_whatsapp()

def send_message(message):
    try:
        input_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']")
        time.sleep(2)
        input_box.send_keys(message + Keys.ENTER)
    except AttributeError:
        raise Exception("Invalid object could be due to invalid URL")
    
def last_message():
    print("read last")
    last_message = "Do you want to..."
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.message-out")))
    while last_message == "Do you want to...":
        message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")

        last_message_element = message_elements[-1]
        # Extract the text content of the last message
        last_message_text = last_message_element.text
        last_message = last_message_text.strip().split("\n")
        last_message = last_message[0]
        if last_message == "Insert new exercise":
            last_message = "What muscle?"
    return last_message

def wait_refresh(last_message_text):
    print("starting refresh")
    print(f"refresh sees last message as {last_message_text}")
    break_line = "--------"
    send_message(break_line)
    while True:
        divs = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='msg-container']")
        last_message_ele = divs[-1].text
        last_message_ele = last_message_ele.strip().split("\n")
        last_message_ele = last_message_ele[0]
        if last_message_ele != break_line:
            break
    print("finished refresh")
    return last_message_ele

def send_and_wait(message, last_message_sent):
    send_message(message)
    returned_message = wait_refresh(last_message_sent)
    # returned_message = last_message(driver)
    return returned_message
