
from fuzzywuzzy import fuzz
from itertools import zip_longest
from muscle_machine_names import MACHINES, MUSCLES, EXERCISE_NAME
from whatsapp import send_and_wait, send_message, driver


def send_and_receive_exercise_details():
    message = "Please now answer all the questions in regards to the exercise"
    send_message(message)
    message = """What is the name of this exercise?"""
    exercise_name = send_and_wait(message, message)
    message = """Please enter the machine/equipment required\nSuch as Lat pull down, Barbell, Seated parallel row machine, Dumbbells\n
    If multiple equipment is needed, please separate equipment with 'and'"""
    # the and split it 
    #split it 
    machine = send_and_wait(message, "If multiple equipment is needed, please separate equipment with 'and'")
    machine_list = split_machine(machine)
    message = "What is the intensity of the exercise?\n1 being not intense and 3 being very intense"
    intensity = send_and_wait(message, "1 being not intense and 3 being very intense")
    message = "What is the optimum level of the exercise?\n1 being not optimum and 3 being very optimum"
    optimum = send_and_wait(message, "1 being not optimum and 3 being very optimum")
    message = "What are some tips for the exercise?"
    tips = send_and_wait(message, message)
    message = "Please enter a link to a picture or video for the exercise"
    link = send_and_wait(message, message)
    return machine_list, intensity, optimum, tips, link, exercise_name

def split_machine(machine):
    machine_list = machine.split("and")
    stripped_machine= []
    print(f"Inside split machine {machine_list}")
    for item in machine_list:
        stripped_machine.append(item.strip())
    print(f"stripped machine {stripped_machine}")
    return stripped_machine

def find_muscle_group(muscle_to_check): 
    for muscle, muscle_list in MUSCLES.items():
        for item in muscle_list:
            if fuzz.partial_ratio(muscle_to_check.lower(), item.lower()) >=85:
                return item, muscle
    send_and_wait(f"What muscle group does {muscle_to_check}")


def check_exercise_details(machine_list, intensity, optimum, tips, link, formated_muscle, muscle_group, exercise_name):
    #check machine
    for machine in machine_list:
        if machine == None or machine == "" :
            return False
    if tips == None or tips == "" or link == None or link == "" or exercise_name == None or exercise_name == "":
        print("here")
        print(f"{tips}_{link}_{exercise_name}")
        return False
    try:
        intensity = int(intensity)
        optimum = int(optimum)
        if intensity > 3 or intensity < 0 or optimum > 3 or optimum < 0:
            raise ValueError
    except ValueError as err:
        print(err)
        return False
    
def format_machine_exercise(inputted_machine_list, inputted_exercise):
    similar_machine = []
    similar_exercise = []
    updated_machine_list = []
    updated_machine = ""
    updated_exercise = ""
    for input_machine in inputted_machine_list:
        for machine in MACHINES:
            if fuzz.partial_ratio(machine.lower(), input_machine.lower()) > 65:
                print(f"format, similar equipment found {machine}")
                similar_machine.append(machine)
            if fuzz.partial_ratio(machine.lower(), input_machine.lower()) > 90:
                print(f"format, equipment found {machine}")
                updated_machine = machine
        if updated_machine == "":
            print(f"found similar about to call redefined {similar_machine}")
            updated_machine_list.append(redefined_variables(similar_machine, "machine"))
        similar_machine = []
    for exericse, exericse_list in EXERCISE_NAME.items():
        for name in exericse_list:
            if fuzz.partial_ratio(name.lower(), inputted_exercise.lower()) > 65:
                similar_exercise.append(name)
            if fuzz.partial_ratio(name.lower(), inputted_exercise.lower()) > 90:
                updated_exercise = name

    if updated_exercise == "":
        updated_exercise = redefined_variables(similar_exercise, "exercise")
    print(updated_machine_list)
    print(updated_exercise)
    return updated_machine_list, updated_exercise

def redefined_variables(similar_list, item_type):
    message = f"""From the list of {item_type}, please send the closest {item_type} to the one you mentioned.\n
    If none match, please re-enter your {item_type}\n{', '.join(similar_list)}"""
    updated_item = send_and_wait(message, f"{', '.join(similar_list)}")
    return updated_item

def current_lift(exercise_name):
    message = f"Please now answer all the questions in regards to your lift for {exercise_name}"
    send_message(message)
    message = """What is the max weight you achieved? in kg"""
    weight = send_and_wait(message, message)
    send_message("Wooow (muscle emoji here but can't insert them")
    message = """What is the max reps your achieved? just enter the number"""
    reps = send_and_wait(message, message)
    send_message("gainsss")
    return weight, reps