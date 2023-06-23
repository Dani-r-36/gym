from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from fuzzywuzzy import fuzz
from muscle_details import find_muscle_group, BACKS, BICEPS, CHESTS, TRICEPS, LEGS, SHOULDERS

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

def start_sess(driver):
    print("riunning")
    time.sleep(5)
    # message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
    message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
    time.sleep(5)
    last_message_element = message_elements[-1]
    # Extract the text content of each message
    message_text = last_message_element.text
    message = message_text.strip().split("\n")
    message = message[0]
    print (message)
    if message == "sess" or message == "Sess":
        record_sess(driver)
        # print(message_text)

def record_sess(driver):
    print("running sess")
    intro_sess(driver)
    muscle = last_message(driver)
    print(f"they said {muscle}")
    formated_muscle = find_muscle_group(muscle)
    message = f"I'll look up your exercises for {formated_muscle}__"
    send_message(driver, message)

def intro_sess(driver):
    send_message(driver, "What muscle?")
    time.sleep(2)
    send_message(driver, f"Here are some examples\nBack\n{BACKS}\nChest\n{CHESTS}\nLegs\n{LEGS}\nShoulders\n{SHOULDERS}\nBiceps\n{BICEPS}\nTricps\n{TRICEPS}")
    time.sleep(15)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.message-out")))

def last_message(driver):
    print("read last")
    last_message = "What muscle?"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.message-out")))
    while last_message == "What muscle?":
        message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")

        last_message_element = message_elements[-1]
        # Extract the text content of the last message
        last_message_text = last_message_element.text
        last_message = last_message_text.strip().split("\n")
        last_message = last_message[0]
        if last_message == str(TRICEPS):
            last_message = "What muscle?"
    return last_message

if __name__ == "__main__":
    driver = connect_whatsapp()
    send_message(driver, "Started your tracker")
    while True:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.message-out")))
        start_sess(driver)