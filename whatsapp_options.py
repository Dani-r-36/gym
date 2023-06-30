from whatsapp import connect_whatsapp, send_message, last_message, wait_refresh, send_and_wait, driver
from sql_functions import error_message, sql_insert_data, insert_new_exercise
from muscle_details import find_muscle_group, check_exercise_details, format_machine_exercise, send_and_receive_exercise_details
from muscle_machine_names import MUSCLES
from whatsapp_messages import INTRO, MUSCLE_EXAMPLE, WHICH_SUB
import time
from fuzzywuzzy import fuzz
from selenium.webdriver.common.by import By

def start_sess():
    print("running")
    time.sleep(5)
    # message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
    message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
    time.sleep(5)
    last_message_element = message_elements[-1]
    # Extract the text content of each message
    message_text = last_message_element.text
    message = message_text.strip().split("\n")
    message = message[0]
    if message == "sess" or message == "Sess":
        record_sess()

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
    returned_message = wait_refresh("End session?")
    return returned_message
    
def choice(user_choice):
    if fuzz.partial_ratio(user_choice, "Find exercises for a muscle") > 70:
        find_exercise()
    # if fuzz.partial_ratio(user_choice, "Find current lift") > 70:
    #     find_current_list(driver)
    if fuzz.partial_ratio(user_choice, "Insert new exercise") > 70:
        machine, intensity, optimum, tips, link, formated_muscle, muscle_group, exercise_name, user_request = get_new_exercise_details()
        print("about to call insert")
        insert_new_exercise(machine, intensity, optimum, tips, link, formated_muscle, muscle_group, exercise_name, user_request)
    if fuzz.partial_ratio(user_choice, "End session") > 70:
        send_message("You look bigger than you think")
        return "End"
    return "Loop"

def find_exercise():
    send_message(MUSCLE_EXAMPLE)
    time.sleep(15)
    last_message_read = wait_refresh(message)
    print(f"they said {last_message_read}")
    formated_muscle, muscle_group = find_muscle_group(last_message_read)
    message = f"I'll look up your exercises for {formated_muscle} which is part of the {muscle_group} group"
    send_message(message)
    #need to search for exercises but first need to insert them
    
def get_new_exercise_details():
    muscle = send_and_wait(WHICH_SUB, f"Tricps: {', '.join(MUSCLES['TRICEPS'])}")
    print(f"they said {muscle}")
    formated_muscle, muscle_group = find_muscle_group(muscle)
    machine, intensity, optimum, tips, link, exercise_name = send_and_receive_exercise_details()

    print(f"machine is {machine}, intensity is {intensity}, optimum is {optimum}, tips: {tips}, link: {link}\n {formated_muscle, muscle_group}")

    if check_exercise_details(machine, intensity, optimum, tips, link, formated_muscle, muscle_group, exercise_name) == False:
        send_message("Incorrect information given, please enter details again")
        get_new_exercise_details()
    #before running need to return all exercises to make sure not already there by checking table
    machine, exercise_name = format_machine_exercise(machine, exercise_name)

    message = """Would you also like to add your max weight and max reps for this exercise?
    \nEnter Yes if you would like to do so, and No if not"""
    user_request = send_and_wait(message, "Enter Yes if you would like to do so, and No if not")
    return machine, intensity, optimum, tips, link, formated_muscle, muscle_group, exercise_name, user_request



if __name__ == "__main__":
    send_message("Started your tracker")
    return_message = wait_refresh("Started your tracker")
    print("out of it ")
    if return_message == "Sess" or return_message == "sess":
        record_sess()
        # start_sess(driver)