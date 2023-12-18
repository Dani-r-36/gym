from whatsapp_commands import  send_message, send_and_wait, handle_error_input
from format_details import find_muscle_group, check_exercise_details, format_machine_exercise, num_integer, split_machine
from sql_functions import existing_exercise
from extract_info import which_sub, get_muscle_id, get_muscles, get_machines, get_machine_id
from long_text.whatsapp_messages import CHECK_INPUT


class ExerciseDetails:
    def __init__(self) -> None:
        self.return_message = ""

    def send_and_receive_exercise_details(self):
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

    def number_muscles(self):
        """Finds num of muscles to cover, making sure they entered int"""
        message = "How many sub-muscle groups does the exercise cover?"
        send_message(which_sub())
        num = send_and_wait(message)
        while num_integer(num) == False:
            handle_error_input("Non integer entered")
            message = "Enter an integer for sub-muscle groups covered"
            num = send_and_wait(message)
        print(f"they entered {num} of sub muscles")
        return num

    def sub_muscle_groups(self, num):
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

    def gather_known_ids(self, details):
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

    def get_new_exercise_details(self, muscle_list, muscle_group):
        """Gathers exercises details via other functions and does app checks. Also checks if weights to be added"""
        details = self.send_and_receive_exercise_details()
        print("the muscle list putting in details is ", muscle_list)
        details["muscle_list"]= muscle_list
        details["muscle_group"]= muscle_group
        # break down of function to perform checks 
        details["machine_list"], details["exercise_name"] = self.exercise_check(details)
        if details['machine_list']== False:
            return False, False
        
        # Checks if user wants to add lift weights and reps
        message = """Would you also like to add your max weight and max reps for this exercise?
        \nEnter Yes if you would like to do so, and No if not"""
        user_request = send_and_wait(message)
        print("about to switch ids")
        # finds muscle and machine ids, as already in DB but needed before hand for internal checks
        details = self.gather_known_ids(details)
        print("switched ids")
        return details, user_request

    def exercise_check(self,details):
        """Performs checks on exercise details (including formatting) and confirms if all correct with user"""
        if check_exercise_details(details) == False:
            handle_error_input("One or more information in exercise is incorrect")
            self.get_new_exercise_details(details["muscle_list"], details["muscle_group"])
        details["machine_list"], details["exercise_name"] = format_machine_exercise(details["machine_list"], details["exercise_name"], get_machines())
        check_print = CHECK_INPUT.format(details["exercise_name"],details["machine_list"],details["intensity"],details["optimum"],details["tips"],details["link"],details["muscle_list"],details["muscle_group"])
        send_message(check_print)
        print(check_print)

        # Checks with user if all entered details is correct
        check = send_and_wait("Is this correct? Enter Y or N")
        if check in ["N","No","no","n"]:
            self.get_new_exercise_details(details["muscle_list"], details["muscle_group"])

        # Before running need to return all exercises to make sure not already there by checking table
        response = existing_exercise(details["exercise_name"])
        if response != False:
            print("similar exercise in database")
            handle_error_input(f"We found similar exercise(s) to the one you entered,\n{response}") 
            return False, False
        return details["machine_list"], details["exercise_name"]