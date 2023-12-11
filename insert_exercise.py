from whatsapp import connect_whatsapp, send_message, send_and_wait
from muscle_details import find_muscle_group, check_exercise_details, format_machine_exercise, send_and_receive_exercise_details, num_integer
from sql_functions import existing_exercise
from extract_info import which_sub, get_muscle_id, get_muscles, get_machines, get_machine_id
from whatsapp_messages import CHECK_INPUT

def number_muscles():
    message = "How many sub-muscle groups does the exercise cover?"
    send_message(which_sub())

    num = send_and_wait(message)
    while num_integer(num) == False:
        send_message("Enter an integer for the number of sub-muscle groups covered") 
        num = send_and_wait(message)
    print(f"they entered {num} of sub muscles")
    return num

def sub_muscle_groups(num):
    i = 0
    muscle_list = []
    muscle_id = []
    muscle_dict = get_muscles()
    which_message = which_sub()
    for i in range(int(num)):
        muscle_num = i + 1
        print(f"running sub group call {muscle_num}")
        muscle = send_and_wait(f"Enter sub muscle {muscle_num}")
        print(f"they said {muscle}")
        formated_muscle, muscle_group = find_muscle_group(muscle, muscle_dict, which_message)
        muscle_list.append(formated_muscle)
    return muscle_list, muscle_group

def get_new_exercise_details(muscle_list, muscle_group):
    machine_ids=[]
    details = send_and_receive_exercise_details()
    print("the muscle list putting in details is ", muscle_list)
    details["muscle_list"]= muscle_list
    details["muscle_group"]= muscle_group
    # break down of function to perform checks 
    details["machine_list"], details["exercise_name"] = exercise_check(details)
    if details['machine_list']== False:
        return False, False
    message = """Would you also like to add your max weight and max reps for this exercise?
    \nEnter Yes if you would like to do so, and No if not"""
    user_request = send_and_wait(message)
    print("asdfasdf about to switch ids")
    details = gather_known_ids(details)
    print("switched ids")
    return details, user_request

def exercise_check(details):
    if check_exercise_details(details) == False:
        send_message("Incorrect information given, please enter details again")
        get_new_exercise_details(details["muscle_list"], details["muscle_group"])
    details["machine_list"], details["exercise_name"] = format_machine_exercise(details["machine_list"], details["exercise_name"], get_machines())
    check_print = CHECK_INPUT.format(details["exercise_name"],details["machine_list"],details["intensity"],details["optimum"],details["tips"],details["link"],details["muscle_list"],details["muscle_group"])
    send_message(check_print)
    print(check_print)
    check = send_and_wait("Is this correct? Enter Y or N")
    if check == "N" or check =="No":
        get_new_exercise_details(details["muscle_list"], details["muscle_group"])
    #before running need to return all exercises to make sure not already there by checking table
    response = existing_exercise(details["exercise_name"])
    if response != False:
        print("similar exercise in database")
        send_message(f"We found similar exercise(s) to the one you entered,\n{response}\nYou can check or add more recent lifts to this exercise by going back to main menu.") 
        return False, False
    return details["machine_list"], details["exercise_name"]

def gather_known_ids(details):
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
