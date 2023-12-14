
from fuzzywuzzy import fuzz
from itertools import zip_longest
from muscle_machine_names import EXERCISE_NAME
from whatsapp import send_and_wait, send_message


def send_and_receive_exercise_details():
    """Gathers all the details about exercises and returns dict"""
    message = "Please now answer all the questions in regards to the exercise"
    send_message(message)
    message = """What is the name of this exercise?"""
    exercise_name = send_and_wait(message)
    message = """Please enter the machine/equipment required\nSuch as Lat pull machine, Barbell, Seated parallel row machine, Dumbbells\n
    If multiple equipment is needed, please separate equipment with 'and'"""
    machine = send_and_wait(message)
    machine_list = split_machine(machine)
    message = "What is the intensity of the exercise?\n1 being not intense and 3 being very intense"
    intensity = send_and_wait(message)
    message = "What is the optimum level of the exercise?\n1 being not optimum and 3 being very optimum"
    optimum = send_and_wait(message)
    message = "What are some tips for the exercise?"
    tips = send_and_wait(message)
    message = "Please enter a link to a picture or video for the exercise"
    link = send_and_wait(message)
    details = {"machine_list": machine_list,"intensity": intensity,"optimum": optimum,"tips": tips,"link": link,"exercise_name": exercise_name, "muscle_list":None,"muscle_group":None}
    return details

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
        send_message(f"We could not find {muscle_to_check} in our list below.")
        send_message(which_message)
        response = send_and_wait(f"Please try to match the muscle to one in the group")
        return find_muscle_group(response, muscle_dict, which_message)


def check_exercise_details(details):
    """Checks machine if in DB and if other new exercises details pass basic checks"""
    for machine in details["machine_list"]:
        if machine == None or machine == "" :
            send_message("Invalid Machine given")
            return False
    if details["tips"] == None or details["tips"] == "" or details["link"] == None or details["link"] == "" or details["exercise_name"] == None or details["exercise_name"] == "":
        print("here")
        print(f"{details['tips']}_{details['link']}_{details['exercise_name']}")
        send_message("No tips, link or exercise name given")
        return False
    try:
        details["intensity"] = int(details["intensity"])
        details["optimum"] = int(details["optimum"])
        if details["intensity"] > 3 or details["intensity"] < 0 or details["optimum"] > 3 or details["optimum"] < 0:
            raise ValueError
    except ValueError as err:
        send_message("Invalid response for intensity or optimum ")
        print(err)
        return False
    
def format_machine_exercise(inputted_machine_list, inputted_exercise, machines):
    """Checks machines and exercises from existing list and formats it if same, or checks if it is a similar one"""
    similar_machine = []
    similar_exercise = []
    updated_machine_list = []
    updated_machine = ""
    updated_exercise = ""

    # For machine\exercise we check if fuzz match greater than 65 then add to list and redefined to find machine\exercise, if exact match we use that
    for input_machine in inputted_machine_list:
        for machine in machines:
            print(f"comparing machine {machine} to {input_machine.lower()} got score {fuzz.partial_ratio(machine.lower(), input_machine.lower())}")
            if fuzz.partial_ratio(machine.lower(), input_machine.lower()) > 65:
                print(f"format, equipment found {machine}")
                similar_machine.append(machine)
            if machine.lower() == input_machine.lower():
                updated_machine = machine
                
        if updated_machine == "":
            print(f"found similar about to call redefined {similar_machine}")
            updated_machine_list.append(redefined_variables(similar_machine, "machine", input_machine))
        similar_machine = []

    for exericse, exericse_list in EXERCISE_NAME.items():
        for name in exericse_list:
            if fuzz.partial_ratio(name.lower(), inputted_exercise.lower()) > 65:
                similar_exercise.append(name)
            if name.lower()== inputted_exercise.lower():
                print("\n\nFound exact exercise")
                updated_exercise = name

    if updated_exercise == "":
        print("\nfinding similar exercises")
        print(f"\nsimilar exercises are {similar_exercise}")
        updated_exercise = redefined_variables(similar_exercise, "exercise", inputted_exercise)
    print(updated_machine_list)
    print(updated_exercise)
    return updated_machine_list, updated_exercise

def redefined_variables(similar_list, item_type, inputted):
    """Has list of similar exercises/machines to what user entered and checks if it is that or user giving new one"""
    if len(similar_list) == 0:
        message = f"""Nothing matched in our list of {item_type}.\nPlease re-enter {item_type} with no typos, you entered {inputted}"""
        updated_item = send_and_wait(message)
    else:
        message = f"""From the list of {item_type}, please send the closest {item_type} to what you entered, {inputted}.
        \n{', '.join(similar_list)}.\nIf none match, please re-enter your {item_type}"""
        updated_item = send_and_wait(message)
    
    if isinstance(updated_item, str) and updated_item.isalpha():
        return updated_item
    else:
        send_message("Enter a valid exercise which is only string")
        return redefined_variables(similar_list, item_type, inputted)

def current_lift(exercise_name):
    """Gathers weight and reps for exercise"""
    message = f"Please now answer all the questions in regards to your lift for {exercise_name}"
    send_message(message)
    message = """What is the max weight you achieved? in kg"""
    weight = send_and_wait(message)
    if num_integer(weight)== False:
        send_message("Enter valid number only")
        return current_lift(exercise_name)
    send_message("Wooow (muscle emoji here but can't insert them")
    message = """What is the max reps your achieved? just enter the number\n
    F9 meaning failed 9th rep, S9 meaning scrapped 9th rep and JF9 meaning just failed 9th rep"""
    reps = send_and_wait(message)
    send_message("gainsss")
    return weight, reps

def num_integer(input):
    return isinstance(input, int) or (isinstance(input, str) and input.isdigit())
    