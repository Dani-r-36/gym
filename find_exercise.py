from whatsapp import send_message, wait_refresh,send_and_wait
from insert_exercise import number_muscles,sub_muscle_groups
from sql_functions import  exercise_from_muscle, existing_exercise, find_exercise_details

def exercise_locate():
    num = number_muscles()
    muscle_list, muscle_group = sub_muscle_groups(num)
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
    # need to search for exercises but first need to insert them


def all_lifts():
    returned_message = send_and_wait("Enter exercise you wish to find")
    response = existing_exercise(returned_message)
    if response != False and len(response) == 1:
        data = find_exercise_details(response)
        cleaned_data = {
            'intensity': int(data[0]['intensity']),
            'tips': data[0]['tips'],
            'optimum_level': int(data[0]['optimum_level']),
            'link': data[0]['picture_video_link'],
            'max_weight': float(data[0]['max_working_weight']),
            'max_reps': data[0]['max_reps']
        }
        message = f"""Exercise name: {response}, intensity: {cleaned_data['intensity']}, tips: {cleaned_data['tips']}_
        _optimum level: {cleaned_data['optimum_level']}, Link: {cleaned_data['link']}, Max working weight: {cleaned_data['max_weight']}_
        _Max reps: {cleaned_data['max_reps']}"""
        send_message(message)
    if response != False and len(response) > 1:
        send_message(f"We found a list of exercises {response}, Be more specific")
        all_lifts()
    if response == True:
        send_message(f"No exercises matched to {returned_message}, Try again")
    