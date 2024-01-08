# {"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNDgxMTkyNCwiaWF0IjoxNzA0NzI1NTI0LCJqdGkiOiI4MGI3ZjQ3NWVjMjE0MDQ2YjUyMTUxYzA1OGMxZGExOSIsInVzZXJfaWQiOjE5NjE2MX0.NZKjcGxnZGjx3LA2MzTsSQhavZnkwax3QNTP5zXulgI","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA0NzI2MTI0LCJpYXQiOjE3MDQ3MjU1MjQsImp0aSI6ImRiYzEwYjkwODk0OTQ1MjI5NmUwNjNmNzMxZmM3YWJjIiwidXNlcl9pZCI6MTk2MTYxfQ.F69u9Uo5Za59LaA0QweaI_M-yLCX6yJzPj9JjLtmKOQ"}
import requests
WEBSITE ="https://wger.de/api/v2"
API_MUSCLE_ID ={"biceps":1,"shoulders":2, "serratus anterior":3, "chest":4, "triceps":5, "abs":6, "calves":7, "glutes":8, "traps":9, "quads":10, "hamstrings":11, "lats":12, "obliquus":14}

class APIError(Exception):
    """Describes an error triggered by a failing API call."""

    def __init__(self, message: str, code: int=500):
        """Creates a new APIError instance."""
        self.message = message
        self.code = code

def fetch_data(id: int) -> dict:
    """Returns a dict of country data from the API."""
    # response = requests.get(f"https://wger.de/api/v2/muscle/")
    response = requests.get(f"{WEBSITE}/exercise/?muscles={id}&language=2")
    # response = requests.get(f"https://wger.de/api/v2/language")
    if response.status_code == 404:
        raise APIError("Unable to locate.", 404)
    elif response.status_code == 500:
        raise APIError("Unable to connect to server.", 500)
    json = response.json()
    return json['results'][:5]

def muscle_api():
    # send and wait API_muscle_id to get muscle 
    returned_message = "shoulders"
    if returned_message.lower() not in  (key.lower() for key in API_MUSCLE_ID):
        # send message saying error not in list
        muscle_api()
    else:
        id = API_MUSCLE_ID[returned_message.lower()]
        return(fetch_data(id))

def find_muscle(muscle_id: str):
    muscle = None
    for key, value in API_MUSCLE_ID.items():
        if value == muscle_id:
            muscle = key
        break
    return muscle

def split_data(data:list):
    if data == None:
        # send message saying no data for muscle and go to main menu
        pass
    for exercise_information in data:
        muscle = []
        for muscle_id in exercise_information['muscles']:
            muscle.append(find_muscle(muscle_id))
        
        # send message with name, muscle and sub muscle, and equpitment 

data = muscle_api()
print(data)
# for muscles in data:
#     print(f"id: {muscles['id']} long name: {muscles['name']} english name: {muscles['name_en']} link: {WEBSITE}{muscles['image_url_main']}")
# print(fetch_data()['results'])