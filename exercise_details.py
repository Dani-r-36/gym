from whatsapp import connect_whatsapp, send_message, send_and_wait
from muscle_details import find_muscle_group, check_exercise_details, format_machine_exercise, send_and_receive_exercise_details
from sql_functions import existing_exercise
from muscle_machine_names import MUSCLES
from whatsapp_messages import WHICH_SUB, CHECK_INPUT

def number_muscles():
    i = 0
    muscle_list = []
    message = "How many sub-muscle groups does the exercise cover?"
    send_message(WHICH_SUB)
    num = send_and_wait(message)
    while num_integer(num) == False:
        send_message("Enter an integer for the number of sub-muscle groups covered") 
        num = send_and_wait(message)
    print(f"they entered {num} of sub muscles")
    for i in range(int(num)):
        muscle_num = i + 1
        print(f"running sub group call {muscle_num}")
        muscle = send_and_wait(f"Enter sub muscle {muscle_num}")
        print(f"they said {muscle}")
        formated_muscle, muscle_group = find_muscle_group(muscle)
        muscle_list.append(formated_muscle)

    return muscle_list, muscle_group

def num_integer(input):
    return isinstance(input, int) or (isinstance(input, str) and input.isdigit())
    
def get_new_exercise_details(muscle_list, muscle_group):
    details = send_and_receive_exercise_details()
    details["muscle_list"]= muscle_list
    details["muscle_group"]= muscle_group
    check_print = CHECK_INPUT.format(details["exercise_name"],details["machine_list"],details["intensity"],details["optimum"],details["tips"],details["link"],details["muscle_list"],details["muscle_group"])
    print(check_print)
    # break down of function to perform checks 
    details["machine_list"], details["exercise_name"] = exercise_check(details, check_print)
    if details['machine_list']== False:
        return False, False
    message = """Would you also like to add your max weight and max reps for this exercise?
    \nEnter Yes if you would like to do so, and No if not"""
    user_request = send_and_wait(message)
    return details, user_request

def exercise_check(details, check_print):
    if check_exercise_details(details) == False:
        send_message("Incorrect information given, please enter details again")
        get_new_exercise_details(details["muscle_list"], details["muscle_group"])
    details["machine_list"], details["exercise_name"] = format_machine_exercise(details["machine_list"], details["exercise_name"])
    send_message(check_print)
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