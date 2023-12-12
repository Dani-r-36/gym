from whatsapp import send_message, wait_refresh, send_and_wait
from sql_functions import error_message, sql_insert_data, insert_new_exercise, all_exercises, lift_edit
from insert_exercise import number_muscles, get_new_exercise_details, sub_muscle_groups
from find_exercise import exercise_locate, all_lifts
from whatsapp_messages import INTRO

import time
from fuzzywuzzy import fuzz
from selenium.webdriver.common.by import By

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
    if fuzz.partial_ratio(user_choice, "Find exercises for a muscle") > 70:
        if exercise_locate() == True:
            user_locate = send_and_wait("Would you like details for one of the exercises? Enter Y or N")
            if user_locate in ["Yes", "Y", "yes"]:
                exercise_request = all_lifts()
                weight_option(exercise_request['exercise_name'], exercise_request['exercise_id'])
    if fuzz.partial_ratio(user_choice, "Find lifts details") > 70:
        returned_message = send_and_wait("Would you like all the exercises in the database? Enter Y or N")
        if returned_message in ["Y", "YES", "Yes", "yes", "y"]:
            exercises_list = all_exercises()
            send_message(exercises_list)
        exercise_request = all_lifts()
        weight_option(exercise_request['exercise_name'], exercise_request['exercise_id'])
    if fuzz.partial_ratio(user_choice, "Insert new exercise") > 70:
        num = number_muscles()
        muscle_list, muscle_group = sub_muscle_groups(num)
        details, user_request = get_new_exercise_details(muscle_list, muscle_group)
        if details == False:
            return "Loop"
        print("about to call insert")
        insert_new_exercise(details, user_request)
    if fuzz.partial_ratio(user_choice, "End session") > 70:
        send_message("You look bigger than you think <3 ♡")
        time.sleep(5)
        return "End"
    return "Loop"

def weight_option(exercise, id):
    returned_message = send_and_wait(f"Would you like edit the reps or weight for {exercise}? Enter Y or N")
    if returned_message in ["Y", "YES", "Yes", "yes", "y"]:
        lift_edit(exercise, id)
    

if __name__ == "__main__":
    return_message = ""
    send_message("Started your tracker")
    while return_message != "sess" and return_message != "Sess":
        return_message = wait_refresh()   
    print("out of it ")
    print(return_message)
    print("caught message sess")
    record_sess()
    # error checking for non duplicates added to dataabse do 