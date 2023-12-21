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

def log_function_call(func):
    def wrapper (*args, **kwargs):
        print(f"calling function {func.__name__} with args {args}, kwargs {kwargs}")
        result= func(*args, **kwargs)
        return result
    return wrapper

def connect_whatsapp():
    """Inital function, to open web whatsapp in test chrome and also find gym contact"""
    try:
        print("Connecting to whatsapp")
        driver = webdriver.Chrome()
        driver.get(WHATSAPP_URL)
        print("got whatsapp URL")
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
    """Checks web whatsapp page and waits till logged in"""
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
    """Sends message by using keys.enter and css selector"""
    try:
        input_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']")
        time.sleep(2)
        if message != "--------":
            message = f"_{message}_"
        input_box.send_keys(message + Keys.ENTER)
    except AttributeError:
        raise Exception("Invalid object could be due to invalid URL")

def read_last_message():
    # returns last sent message in chat
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.message-out")))
    message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
    last_message = message_elements[-1].text.strip().split("\n")[0]
    return last_message

def wait_refresh():
    """Checks if user sends message by sending break_line and checking if changes"""
    break_line = "--------"
    return_message = break_line
    print("starting refresh")
    message = read_last_message()
    print(f"refresh sees last message as {message}")
    send_message(break_line)
    print("waiting for user message")
    while return_message == break_line:      
        return_message = read_last_message()
    return return_message

@log_function_call
def send_and_wait(message):
    """Calls to send message and then collects entered input from wait_refresh()"""
    send_message(message)
    returned_message = wait_refresh()
    return returned_message.lower()

def handle_error_input(reason):
    send_message(f"Invalid input. Please try again._\n_Reason for invalid input {reason}")