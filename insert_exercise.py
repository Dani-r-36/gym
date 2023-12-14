from whatsapp import connect_whatsapp, send_message, send_and_wait
from muscle_details import find_muscle_group, check_exercise_details, format_machine_exercise, send_and_receive_exercise_details, num_integer
from sql_functions import existing_exercise
from extract_info import which_sub, get_muscle_id, get_muscles, get_machines, get_machine_id
from whatsapp_messages import CHECK_INPUT

def number_muscles():
    """Finds num of muscles to cover, making sure they entered int"""
    message = "How many sub-muscle groups does the exercise cover?"
    send_message(which_sub())
    num = send_and_wait(message)
    while num_integer(num) == False:
        message = "Enter an integer for the number of sub-muscle groups covered"
        send_message(message) 
        num = send_and_wait(message)
    print(f"they entered {num} of sub muscles")
    return num

def sub_muscle_groups(num):
    """Returns formatted muscle and muscle group from one they entered incase of typos"""
    i = 0
    muscle_list = []
    muscle_dict = get_muscles()
    which_message = which_sub()
    for i in range(int(num)):
        muscle_num = i + 1
        print(f"running sub group call {muscle_num}")
        muscle = send_and_wait(f"Enter sub muscle {muscle_num}")
        formated_muscle, muscle_group = find_muscle_group(muscle, muscle_dict, which_message)
        muscle_list.append(formated_muscle)
    return muscle_list, muscle_group

def get_new_exercise_details(muscle_list, muscle_group):
    """Gathers exercises details via other functions and does app checks. Also checks if weights to be added"""
    details = send_and_receive_exercise_details()
    print("the muscle list putting in details is ", muscle_list)
    details["muscle_list"]= muscle_list
    details["muscle_group"]= muscle_group
    # break down of function to perform checks 
    details["machine_list"], details["exercise_name"] = exercise_check(details)
    if details['machine_list']== False:
        return False, False
    
    # Checks if user wants to add lift weights and reps
    message = """Would you also like to add your max weight and max reps for this exercise?
    \nEnter Yes if you would like to do so, and No if not"""
    user_request = send_and_wait(message)
    print("about to switch ids")
    # finds muscle and machine ids, as already in DB but needed before hand for internal checks
    details = gather_known_ids(details)
    print("switched ids")
    return details, user_request

def exercise_check(details):
    """Performs checks on exercise details (including formatting) and confirms if all correct with user"""
    if check_exercise_details(details) == False:
        send_message("Incorrect information given, please enter details again")
        get_new_exercise_details(details["muscle_list"], details["muscle_group"])
    details["machine_list"], details["exercise_name"] = format_machine_exercise(details["machine_list"], details["exercise_name"], get_machines())
    check_print = CHECK_INPUT.format(details["exercise_name"],details["machine_list"],details["intensity"],details["optimum"],details["tips"],details["link"],details["muscle_list"],details["muscle_group"])
    send_message(check_print)
    print(check_print)

    # Checks with user if all entered details is correct
    check = send_and_wait("Is this correct? Enter Y or N")
    if check in ["N","No","no","n"]:
        get_new_exercise_details(details["muscle_list"], details["muscle_group"])

    # Before running need to return all exercises to make sure not already there by checking table
    response = existing_exercise(details["exercise_name"])
    if response != False:
        print("similar exercise in database")
        send_message(f"We found similar exercise(s) to the one you entered,\n{response}\nYou can check or add more recent lifts to this exercise by going back to main menu.") 
        return False, False
    return details["machine_list"], details["exercise_name"]

def gather_known_ids(details):
    """Gets muscle and machine id in DB from their names"""
    muscle_id = []
    machine_ids = []
    for muscles in details['muscle_list']:
        print("in the list of muscles it is ",muscles)
        formated_muscle, muscle_group = get_muscle_id(muscles)
        muscle_id.append(formated_muscle)
    for machine in details['machine_list']:
        machine_ids.append(get_machine_id(machine))
    details['muscle_list'] = muscle_id
    details['muscle_group'] = muscle_group
    details['machine_list'] = machine_ids
    return details
