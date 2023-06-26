from whatsapp import connect_whatsapp, send_message, start_sess, last_message, wait_refresh
from muscle_details import find_muscle_group, BACKS, BICEPS, CHESTS, TRICEPS, LEGS, SHOULDERS
import time
from fuzzywuzzy import fuzz

def record_sess(driver):
    print("running sess")
    intro_sess(driver)
    user_choice = last_message(driver)
    print(f"they said {user_choice}")
    choice(driver, user_choice)

def intro_sess(driver):
    intro = """
    Do you want to...\nFind exercises for a muscle?\n
    Find your current lift for an exercise?\n
    Insert a new exercise?"""
    send_message(driver, intro)
    time.sleep(2)
    
def choice(driver, user_choice):
    if fuzz.partial_ratio(user_choice, "Find exercises for a muscle") > 70:
        find_exercise(driver)
    # if fuzz.partial_ratio(user_choice, "Find current lift") > 70:
    #     find_current_list(driver)
    if fuzz.partial_ratio(user_choice, "Insert new exercise") > 70:
        insert_new_exercise(driver)

def find_exercise(driver):
    send_message(driver, f"Here are some examples\nBack: {', '.join(BACKS)}\nChest: {', '.join(CHESTS)}\nLegs: {', '.join(LEGS)}\nShoulders: {', '.join(SHOULDERS)}\nBiceps: {', '.join(BICEPS)}\nTricps: {', '.join(TRICEPS)}")
    time.sleep(15)
    wait_refresh(driver)
    muscle = last_message(driver)
    print(f"they said {muscle}")
    formated_muscle = find_muscle_group(muscle)
    message = f"I'll look up your exercises for {formated_muscle}"
    send_message(driver, message)
    #need to search for exercises but first need to insert them

def insert_new_exercise(driver):
    

if __name__ == "__main__":
    driver = connect_whatsapp()
    send_message(driver, "Started your tracker")
    while True:
        wait_refresh(driver)
        start_sess(driver)