
from whatsapp_commands import send_message, send_and_wait, handle_error_input
from sql_functions import  insert_new_exercise, all_exercises, lift_edit
from find_exercise import exercise_locate, all_lifts
from new_exercise import ExerciseDetails
from api import muscle_api, split_data
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'long_text'))
from whatsapp_messages import INTRO

import time
from fuzzywuzzy import fuzz


class GymTracker:

    def __init__(self) -> None:
        self.return_message = ""
        self.exercise_details = ExerciseDetails()

    def run(self):
        """Initiates gym tracker after user requests to"""
        while self.return_message.lower() not in ["sess", "end"]:
            self.return_message = send_and_wait("Started your tracker") 
        
        if self.return_message.lower() == "sess":
            self.record_sess()

    def record_sess(self):
        """Starts recording with intro and calls choices"""
        while True:
            print("running sess")
            self.return_message= send_and_wait(INTRO)
            option = self.choice()
            if option == "End":
                break

    def weight_option(self,exercise, id):
        """Provides option to update reps or weight for exercise"""
        self.returned_message = send_and_wait(f"Would you like edit the reps or weight for {exercise}? Enter Y or N")
        if self.returned_message.lower() in ["yes", "y"]:
            lift_edit(exercise, id)
    
    def find_lift(self, lifts):
        """function calls to find exercise details"""
        exercise_request = lifts
        if exercise_request != None:
            self.weight_option(exercise_request['exercise_name'], exercise_request['exercise_id'])
        return "Loop"
    
    def inserting(self):
        """function calls to find exercise details and then gets inserted in DB"""
        num = self.exercise_details.number_muscles()
        muscle_list, muscle_group = self.exercise_details.sub_muscle_groups(num)
        details, user_request = self.exercise_details.get_new_exercise_details(muscle_list, muscle_group)
        if details != False:
            print("about to call insert")
            # Inserts checked details
            insert_new_exercise(details, user_request)
        return "Loop"
   
    def choice(self):
        """Provides 4 options for the user"""
        # First two option also allow user to edit weight lifted for exercise, using weight_option

        # Finds exercises for muscle by first checking if exercises for muscles exist, and gives details for them
        if fuzz.partial_ratio(self.return_message, "Find exercises for a muscle") > 80:
            if exercise_locate() == True:
                message = "Would you like details for one of the exercises? Enter Y or N"
                self.return_message = send_and_wait(message)
                if self.return_message.lower() in ["y", "yes"]:
                    return self.find_lift(all_lifts())
                
        # Find exercises details, from using all_lifts()
        elif fuzz.partial_ratio(self.return_message, "Find lifts details") > 80:
            message = "Would you like all the exercises in the database? Enter Y or N"
            self.return_message = send_and_wait(message)
            if self.return_message.lower() in ["yes", "y"]:
                exercises_list = all_exercises()
                send_message(exercises_list)
            return self.find_lift(all_lifts())

        # Main option to insert exercise by first finding number of muscles, which muscles, then details and then inserts into DB
        elif fuzz.partial_ratio(self.return_message, "Insert new exercise") > 80:
            return self.inserting()

        elif fuzz.partial_ratio(self.return_message, "Find new exercise") > 80:
            print("calling api")
            returned_data = muscle_api()
            return split_data(returned_data)

        # Stops the whatsapp bot and ends session
        elif fuzz.partial_ratio(self.return_message, "End session") > 70:
            send_message("You look bigger than you think <3")
            time.sleep(5)
            return "End"
        else:
            handle_error_input("Not one of the options provided")
        return "Loop"

if __name__ == "__main__":
    gym_tracker = GymTracker()
    gym_tracker.run()