from whatsapp import send_message, send_and_wait
from sql_functions import  insert_new_exercise, all_exercises, lift_edit
from insert_exercise import number_muscles, get_new_exercise_details, sub_muscle_groups
from find_exercise import exercise_locate, all_lifts
from whatsapp_messages import INTRO

import time
from fuzzywuzzy import fuzz
from selenium.webdriver.common.by import By

def record_sess():
    """Starts recording with intro and calls choices"""
    while True:
        print("running sess")
        user_choice = send_and_wait(INTRO)
        option = choice(user_choice)
        if option == "End":
            break

    
def choice(user_choice):
    """Provides 4 options for the user"""

    # First two option also allow user to edit weight lifted for exercise, using weight_option

    # Finds exercises for muscle by first checking if exercises for muscles exist, and gives details for them
    if fuzz.partial_ratio(user_choice, "Find exercises for a muscle") > 70:
        if exercise_locate() == True:
            message = "Would you like details for one of the exercises? Enter Y or N"
            user_locate = send_and_wait(message)
            if user_locate in ["Yes", "Y", "yes"]:
                exercise_request = all_lifts()
                if exercise_request == None:
                    return "Loop"
                weight_option(exercise_request['exercise_name'], exercise_request['exercise_id'])
    # Find exercises details, from using all_lifts()
    if fuzz.partial_ratio(user_choice, "Find lifts details") > 70:
        message = "Would you like all the exercises in the database? Enter Y or N"
        returned_message = send_and_wait(message)
        if returned_message in ["Y", "YES", "Yes", "yes", "y"]:
            exercises_list = all_exercises()
            send_message(exercises_list)
        exercise_request = all_lifts()
        if exercise_request == None:
            return "Loop"
        weight_option(exercise_request['exercise_name'], exercise_request['exercise_id'])

    # Main option to insert exercise by first finding number of muscles, which muscles, then details and then inserts into DB
    if fuzz.partial_ratio(user_choice, "Insert new exercise") > 70:
        num = number_muscles()
        muscle_list, muscle_group = sub_muscle_groups(num)
        details, user_request = get_new_exercise_details(muscle_list, muscle_group)
        if details == False:
            return "Loop"
        print("about to call insert")
        # Inserts checked details
        insert_new_exercise(details, user_request)

    # Stops the whatsapp bot and ends session
    if fuzz.partial_ratio(user_choice, "End session") > 70:
        send_message("You look bigger than you think <3 ♡")
        time.sleep(5)
        return "End"
    return "Loop"

def weight_option(exercise, id):
    """Provides option to update reps or weight for exercise"""
    returned_message = send_and_wait(f"Would you like edit the reps or weight for {exercise}? Enter Y or N")
    if returned_message in ["Y", "YES", "Yes", "yes", "y"]:
        lift_edit(exercise, id)
    

if __name__ == "__main__":
    """Main start by waiting for user to enter sess"""
    return_message = ""
    # send_message("Started your tracker")
    while return_message != "sess" and return_message != "Sess":
        return_message = send_and_wait("Started your tracker")   
    print("out of it ")
    print(return_message)
    print("caught message sess")
    record_sess()
    # error checking for non duplicates added to dataabse do 