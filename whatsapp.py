from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def connect_whatsapp():
    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com/')
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.message-in")))
    time.sleep(20)
    # WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-ref]")))
    # time.sleep(15)
    contact_name = "Gym"
    search_box = driver.find_element(By.XPATH, '//*[contains(@class, "selectable-text copyable-text")]')
    search_box.send_keys(contact_name)
    time.sleep(2)  # Wait for search results to load
    chat = driver.find_element(By.XPATH, f"//span[@title='{contact_name}']")
    chat.click()
    time.sleep(2)
    return driver

def send_message(driver, message):
    inp_xpath = '//p[@class, "selectable-text copyable-text"][@contenteditable="true"][@data-tab="1"]'
    input_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']")
    time.sleep(2)
    input_box.send_keys(message + Keys.ENTER)
    
def last_message(driver):
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

def wait_refresh(driver, last_message_text):
    print("starting refresh")
    # locator = (By.ID, 'main')
    print(f"refresh sees last message as {last_message_text}")
    while True:
        divs = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='msg-container']")
        last_message = divs[-1].text
        last_message = last_message.strip().split("\n")
        last_message = last_message[0]
        if last_message != last_message_text:
            break
    print("finished refresh")
    return last_message

def send_and_wait(driver, message, last_message_sent):
    send_message(driver, message)
    time.sleep(5)
    returned_message = wait_refresh(driver, last_message_sent)
    # returned_message = last_message(driver)
    return returned_message

if __name__ == "__main__":
    driver = connect_whatsapp()
    send_message(driver, "Started your tracker")
    while True:
        start_sess(driver)