
from fuzzywuzzy import fuzz
from itertools import zip_longest
from muscle_machine_names import MACHINES, MUSCLES, EXERCISE_NAME
from whatsapp import send_and_wait


def send_and_receive_exercise_details(driver):
    message = "Please now answer all the questions in regards to the exercise"
    temp = send_and_wait(driver, message, message)
    message = """What is the name of this exercise?"""
    exercise_name = send_and_wait(driver, message, message)
    message = """Please enter the machine/equipment required\nSuch as Lat pull down, Barbell, Seated parallel row machine, Dumbbells\n
    If multiple equipment is needed, please separate equipment with 'and'"""
    machine = send_and_wait(driver, message, "If multiple equipment is needed, please separate equipment with 'and'")
    message = "What is the intensity of the exercise?\n1 being not intense and 3 being very intense"
    intensity = send_and_wait(driver, message, "1 being not intense and 3 being very intense")
    message = "What is the optimum level of the exercise?\n1 being not optimum and 3 being very optimum"
    optimum = send_and_wait(driver, message, "1 being not optimum and 3 being very optimum")
    message = "What are some tips for the exercise?"
    tips = send_and_wait(driver, message, message)
    message = "Please enter a link to a picture of video for the exercise"
    link = send_and_wait(driver, message, message)
    return machine, intensity, optimum, tips, link, exercise_name

def find_muscle_group(muscle_to_check): 
    for muscle, muscle_list in MUSCLES.items():
        for item in muscle_list:
            if fuzz.partial_ratio(muscle_to_check.lower(), item.lower()) >=85:
                return item, muscle


def check_exercise_details(machine, intensity, optimum, tips, link, formated_muscle, muscle_group, exercise_name):
    #check machine
    if machine == None or machine == "" or tips == None or tips == "" or link == None or link == "" or exercise_name == None or exercise_name == "":
        print("here")
        print(f"{machine}_{tips}_{link}_{exercise_name}")
        return False
    try:
        intensity = int(intensity)
        optimum = int(optimum)
        if intensity > 3 or intensity < 0 or optimum > 3 or optimum < 0:
            raise ValueError
    except ValueError as err:
        print(err)
        return False
    
def format_machine_exercise(driver, inputted_machine, inputted_exercise):
    similar_machine = []
    similar_exercise = []
    updated_machine = ""
    updated_exercise = ""
    for machine in MACHINES:
        if fuzz.partial_ratio(machine, inputted_machine) > 65:
            similar_machine.append(machine)
        if fuzz.partial_ratio(machine, inputted_machine) > 90:
            updated_machine = machine
    for exericse, exericse_list in EXERCISE_NAME.items():
        for name in exericse_list:
            if fuzz.partial_ratio(name, inputted_exercise) > 65:
                similar_exercise.append(name)
            if fuzz.partial_ratio(name, inputted_exercise) > 90:
                updated_exercise = machine

    if updated_machine == "":
        updated_machine = redefined_variables(driver, similar_machine, "machine")
    if updated_exercise == "":
        updated_exercise = redefined_variables(driver, similar_exercise, "exercise")
    return updated_machine, updated_exercise

def redefined_variables(driver, similar_list, item_type):
    message = f"""From the list of {item_type}, please send the closest {item_type} to the one you mentioned.\n
    If none match, please re-enter your {item_type}\n{', '.join(similar_list)}"""
    updated_item = send_and_wait(driver, message, f"{', '.join(similar_list)}")
    return updated_item