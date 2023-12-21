from whatsapp_commands import send_message,send_and_wait
from new_exercise import ExerciseDetails
from sql_functions import  exercise_from_muscle, existing_exercise, find_exercise_details

def exercise_locate():
    """Gathers num of muscles and which muscles, then checks DB for those details"""
    exercise_details_instance = ExerciseDetails()
    num = exercise_details_instance.number_muscles()
    muscle_list, muscle_group = exercise_details_instance.sub_muscle_groups(num)
    message = f"I'll look up your exercises for {muscle_list} which is part of the {muscle_group} group"
    send_message(message)
    for muscle in muscle_list:
        exercise_name = exercise_from_muscle(muscle, muscle_group)
        if exercise_name == False:
            send_message("Sorry could not find any exercises for those muscles")
            return False
    send_message("These are the Exercises we found")
    send_message(exercise_name)
    return True


def all_lifts():
    """Finds exercise & id if it exists and then finds its details. Returns exercise and id"""
    returned_message = send_and_wait("Enter exercise you wish to find")
    response = existing_exercise(returned_message)
    print("response is ",response)
    if response != False:
        if len(response) == 1:
            """If only exercise found, sorts exercise details into dict and creates message, according to max weight reps not None"""
            data = find_exercise_details(response[0]['exercise_name'])
            if data[0]['max_working_weight'] == None and data[0]['max_reps'] == None:
                cleaned_data = {
                'intensity': int(data[0]['intensity']),
                'tips': data[0]['tips'],
                'optimum_level': int(data[0]['optimum_level']),
                'link': data[0]['picture_video_link'],
                'max_weight': None,
                'max_reps': None
            }
            else:
                cleaned_data = {
                    'intensity': int(data[0]['intensity']),
                    'tips': data[0]['tips'],
                    'optimum_level': int(data[0]['optimum_level']),
                    'link': data[0]['picture_video_link'],
                    'max_weight': float(data[0]['max_working_weight']),
                    'max_reps': data[0]['max_reps']
                }
            message = f"""Exercise name: {response[0]['exercise_name']}, intensity: {cleaned_data['intensity']}, tips: {cleaned_data['tips']}_
            _optimum level: {cleaned_data['optimum_level']}, Link: {cleaned_data['link']}, Max working weight: {cleaned_data['max_weight']}_
            _Max reps: {cleaned_data['max_reps']}"""
            send_message(message)
        else:
            """Multiple exercises returned due to not specific exercise name entered"""
            send_message(f"We found a list of exercises {response}, Be more specific")
            all_lifts()
    else:
        send_message(f"No exercises matched to {returned_message}, Try again")
        return None
    return response[0]
