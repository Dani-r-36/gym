from whatsapp import send_message, wait_refresh, send_and_wait
from sql_functions import error_message, sql_insert_data, insert_new_exercise
from exercise_details import number_muscles, get_new_exercise_details
from sql_functions import existing_exercise
from whatsapp_messages import INTRO

import time
from fuzzywuzzy import fuzz
from selenium.webdriver.common.by import By

def start_sess():
    try:
        print("running")
        time.sleep(5)
        message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
        time.sleep(5)
        last_message_element = message_elements[-1]
        message_text = last_message_element.text
        message = message_text.strip().split("\n")
        message = message[0]
        if message == "sess" or message == "Sess":
            record_sess()
    except IndexError as err :
        print("ERROR")
        print (err)
        print("Couldn't find message elements in find.element in start_sess")

def record_sess():
    while True:
        print("running sess")
        user_choice = intro_sess()
        print(f"they said _{user_choice}_")
        option = choice(user_choice)
        if option == "End":
            break

def intro_sess():
    send_message(INTRO)
    returned_message = wait_refresh()
    return returned_message
    
def choice(user_choice):
    # if fuzz.partial_ratio(user_choice, "Find exercises for a muscle") > 70:
    #     find_exercise()
    # if fuzz.partial_ratio(user_choice, "Find current lift") > 70:
    #     find_current_list(driver)
    if fuzz.partial_ratio(user_choice, "Insert new exercise") > 70:
        muscle_list, muscle_group = number_muscles()
        details, user_request = get_new_exercise_details(muscle_list, muscle_group)
        if details == False:
            return "Loop"
        print("about to call insert")
        insert_new_exercise(details, user_request)
    if fuzz.partial_ratio(user_choice, "End session") > 70:
        send_message("You look bigger than you think")
        return "End"
    return "Loop"

# def find_exercise():
#     send_message(MUSCLE_EXAMPLE)
#     time.sleep(15)
#     last_message_read = wait_refresh(message)
#     print(f"they said {last_message_read}")
#     formated_muscle, muscle_group = find_muscle_group(last_message_read)
#     message = f"I'll look up your exercises for {formated_muscle} which is part of the {muscle_group} group"
#     send_message(message)
    #need to search for exercises but first need to insert them


if __name__ == "__main__":
    return_message = ""
    send_message("Started your tracker")
    while return_message != "sess" and return_message != "Sess":
        return_message = wait_refresh()   
    print("out of it ")
    print(return_message)
    print("caught message sess")
    # check = existing_exercise("lat pulldown with some random shit")
    record_sess()
    # start_sess(driver)