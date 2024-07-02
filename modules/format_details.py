
from fuzzywuzzy import fuzz
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'long_text'))
from muscle_machine_names import EXERCISE_NAME
from whatsapp_commands import send_and_wait, send_message, handle_error_input

def split_machine(machine):
    machine_list = machine.split(" and ")
    stripped_machine= []
    print(f"Inside split machine {machine_list}")
    for item in machine_list:
        stripped_machine.append(item.strip())
    print(f"stripped machine {stripped_machine}")
    return stripped_machine

def find_muscle_group(muscle_to_check, muscle_dict, which_message): 
    """Finds muscle in same format as DB and returns it"""
    muscles_found = []
    exact_muscle, exact_group = "", ""
    for muscle, muscle_list in muscle_dict.items():
        for item in muscle_list:
            if fuzz.partial_ratio(muscle_to_check.lower(), item.lower()) >=85:
                print(f"found item {item} and muscle {muscle}")
                exact_muscle = item
                exact_group = muscle
                muscles_found.append(exact_muscle)
    if len(muscles_found)>0:
        if len(muscles_found)>1:
            response = send_and_wait(f"Please specify which muscle from the list {muscles_found}")
            return find_muscle_group(response, muscle_dict, which_message)
        else:
            return exact_muscle, exact_group
    else:
        handle_error_input(f"Muscle: {muscle_to_check} not matching to our list")
        send_message(which_message)
        response = send_and_wait(f"Please try to match the muscle to one in the group")
        return find_muscle_group(response, muscle_dict, which_message)


def check_exercise_details(details):
    """Checks machine if in DB and if other new exercises details pass basic checks"""
    for machine in details["machine_list"]:
        if machine == None or machine == "" :
            handle_error_input("Invalid Machine given")
            return False
    if details["tips"] == None or details["tips"] == "" or details["link"] == None or details["link"] == "" or details["exercise_name"] == None or details["exercise_name"] == "":
        print("here")
        print(f"{details['tips']}_{details['link']}_{details['exercise_name']}")
        handle_error_input("No tips, link or exercise name given")
        return False
    try:
        details["intensity"] = int(details["intensity"])
        details["optimum"] = int(details["optimum"])
        if details["intensity"] > 3 or details["intensity"] < 0 or details["optimum"] > 3 or details["optimum"] < 0:
            raise ValueError
    except ValueError as err:
        handle_error_input("Invalid response for intensity or optimum ")
        print(err)
        return False

def redefined_variables(similar_list, item_type, inputted):
    """Has list of similar exercises/machines to what user entered and checks if it is that or user giving new one"""
    updated_item = ""
    if len(similar_list) == 0:
        message = f"""Nothing matched in our list of {item_type}.\nPlease re-enter {item_type} with no typos, you entered {inputted}"""
        updated_item = send_and_wait(message)
    else:
        message = f"""From the list of {item_type}, please send the closest {item_type} to what you entered, {inputted}.
        \n{', '.join(similar_list)}.\nIf none match, please re-enter your {item_type}"""
        updated_item = send_and_wait(message)

    alpha_check = updated_item.replace(" ", "")

    if isinstance(alpha_check, str) and alpha_check.isalpha():
        return updated_item
    else:
        handle_error_input("Non-valid string entered for exercise")
        return redefined_variables(similar_list, item_type, inputted)

def machine_check(inputted_machine_list, machines):
    """checks inputted machine if in database"""
    similar_machine = []
    updated_machine_list = []
    updated_machine = ""
    for input_machine in inputted_machine_list:
        for machine in machines:
            score = fuzz.partial_ratio(machine.lower(), input_machine.lower())
            print(f"comparing machine {machine} to {input_machine.lower()} got score {score}")
            if score > 70:
                print(f"format, equipment found {machine}")
                similar_machine.append(machine)
            if machine.lower() == input_machine.lower():
                updated_machine = machine
                updated_machine_list.append(updated_machine)

        if updated_machine == "":
            if len(similar_machine)>0:
                print(f"found similar about to call redefined {similar_machine}")
                updated_machine_list.append(redefined_variables(similar_machine, "machine", input_machine))
            else:
                updated_machine_list.append(input_machine)
        similar_machine = []
        updated_machine = ""
    return updated_machine_list

def exercise_check(inputted_exercise):
    """checks if exercise is in local list"""
    similar_exercise = []
    updated_exercise = ""
    for exericse, exericse_list in EXERCISE_NAME.items():
        for name in exericse_list:
            if fuzz.partial_ratio(name.lower(), inputted_exercise.lower()) > 65:
                similar_exercise.append(name)
            if name.lower()== inputted_exercise.lower():
                print("\n\nFound exact exercise")
                updated_exercise = name

    if updated_exercise == "":
        if len(similar_exercise)>0:
            print("\nfinding similar exercises")
            print(f"\nsimilar exercises are {similar_exercise}")
            updated_exercise = redefined_variables(similar_exercise, "exercise", inputted_exercise)
        else:
            updated_exercise = inputted_exercise
    return updated_exercise

def format_machine_exercise(inputted_machine_list, inputted_exercise, machines):
    """Checks machines and exercises from existing list and formats it if same, or checks if it is a similar one"""
    # For machine\exercise we check if fuzz match greater than 65 then add to list and redefined to find machine\exercise, if exact match we use that
    updated_machine_list = machine_check(inputted_machine_list, machines)
    updated_exercise = exercise_check(inputted_exercise)
    print(updated_machine_list)
    print(updated_exercise)
    return updated_machine_list, updated_exercise

def current_lift(exercise_name):
    """Gathers weight and reps for exercise"""
    message = f"Please now answer all the questions in regards to your lift for {exercise_name}"
    send_message(message)
    message = """What is the max weight you achieved? in kg"""
    weight = send_and_wait(message)
    if num_integer(weight)== False:
        send_message("Enter number only")
        return current_lift(exercise_name)
    send_message("Wooow (muscle emoji here but can't insert them")
    message = """What is the max reps your achieved?_\n_
    F9 meaning failed 9th rep, S9 meaning scrapped 9th rep and JF9 meaning just failed 9th rep"""
    reps = send_and_wait(message)
    send_message("gainsss")
    return weight, reps

def num_integer(input):
    return isinstance(input, int) or (isinstance(input, str) and input.isdigit())
    