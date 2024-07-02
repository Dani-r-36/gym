# {"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNDgxMTkyNCwiaWF0IjoxNzA0NzI1NTI0LCJqdGkiOiI4MGI3ZjQ3NWVjMjE0MDQ2YjUyMTUxYzA1OGMxZGExOSIsInVzZXJfaWQiOjE5NjE2MX0.NZKjcGxnZGjx3LA2MzTsSQhavZnkwax3QNTP5zXulgI","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0NzI2MTI0LCJpYXQiOjE3MDQ3MjU1MjQsImp0aSI6ImRiYzEwYjkwODk0OTQ1MjI5NmUwNjNmNzMxZmM3YWJjIiwidXNlcl9pZCI6MTk2MTYxfQ.F69u9Uo5Za59LaA0QweaI_M-yLCX6yJzPj9JjLtmKOQ"}
import requests
from whatsapp_commands import send_message, send_and_wait, handle_error_input
from langdetect import detect

WEBSITE ="https://wger.de/api/v2"
API_MUSCLE_ID ={"biceps":1,"shoulders":2, "serratus anterior":3, "chest":4, "triceps":5, "abs":6, "calves":7, "glutes":8, "traps":9, "quads":10, "hamstrings":11, "lats":12, "obliquus":14}
API_EQUIP_ID = {"barbell":1, "bench":8, "dumbbell":3, "gym mat":4, "incline bench":9, "kettlebell":10, "pull-up bar":6, "ez-bar":2, "swiss ball":5, "none (bodyweight exercise)":7}

class APIError(Exception):
    """Describes an error triggered by a failing API call."""

    def __init__(self, message: str, code: int=500):
        """Creates a new APIError instance."""
        self.message = message
        self.code = code

def fetch_data(id: int) -> dict:
    """Returns a dict of country data from the API."""
    response = requests.get(f"{WEBSITE}/exercise/?muscles={id}&language=2")
    if response.status_code == 404:
        raise APIError("Unable to locate.", 404)
    elif response.status_code == 500:
        raise APIError("Unable to connect to server.", 500)
    json = response.json()
    return json['results'][:10]

def muscle_api():
    formatted_muscle_keys = ', '.join(API_MUSCLE_ID.keys())
    send_message(f"These are the muscles in the API._\n_{formatted_muscle_keys}")
    returned_message = send_and_wait("Please enter the muscle you wish to find an exercise for")
    if returned_message.lower() not in  (key.lower() for key in API_MUSCLE_ID):
        handle_error_input("Entry not in API")
        muscle_api()
    else:
        id = API_MUSCLE_ID[returned_message.lower()]
        return(fetch_data(id))

def find_muscle_equip(id: str, hash_table: dict):
    item = None
    for key, value in hash_table.items():
        if value == id:
            item = key
            break
    return item

def split_data(data:list):
    passed_exercises = 0
    if data == None:
        return handle_error_input("No data for muscle in API")
    send_message("These are the some exercises we found._\n_NOTE THERE MAYBE SOME ERROR WITH THE DATA FROM THE API SUCH AS DIFFERENT LANGUAGE.")
    for exercise_information in data:
        try:
            if passed_exercises ==5:
                break
            if detect(exercise_information['description']) == 'en':
                passed_exercises +=1
                muscle = []
                for muscle_id in exercise_information['muscles']:
                    muscle.append(find_muscle_equip(muscle_id, API_MUSCLE_ID))
                equip = []
                for equip_id in exercise_information['muscles']:
                    equip.append(find_muscle_equip(equip_id, API_EQUIP_ID))
                send_message(f"Name: {exercise_information['name']}, Muscles: {muscle}, Equipment: {equip}, Description: {exercise_information['description']}")
        except Exception as e:
            print(f"error in checking language of api data: {e}")
    return send_message("If no exercises matched, please use other sources")
# data = muscle_api()
# split_data(data)
# print(data)
# json = data.json()
# print(json)

# for muscles in data:
#     print(f"id: {muscles['id']} long name: {muscles['name']} english name: {muscles['name_en']} link: {WEBSITE}{muscles['image_url_main']}")
# print(fetch_data()['results'])


# print(fuzz.partial_ratio("Find new exercise", "Insert new exercise"))