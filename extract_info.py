from sql_code import ALL_GROUP_MUSCLE, ALL_SUB_MUSCLE, ALL_MACHINE, MACHINE_ID, MUSCLE_ID, EXERCISE_ID
from sql_functions import get_db_connection, sql_fetch_existing
from fuzzywuzzy import fuzz

conn = get_db_connection()

def get_muscles():
    group_data = sql_fetch_existing(ALL_GROUP_MUSCLE, None)
    sub_data = sql_fetch_existing(ALL_SUB_MUSCLE,None)
    muscle_dict = {}
    for row in group_data:
        sub_muscle = []
        for muscle in sub_data:
            if row['group_id'] == muscle['group_id']:
                sub_muscle.append(muscle['muscle_name'])
        muscle_dict[row['muscle_group']] = sub_muscle
    return muscle_dict

def find_muscle_group(muscle_to_check): 
    muscle_dict = get_muscles()
    for muscle, muscle_list in muscle_dict.items():
        for item in muscle_list:
            if fuzz.partial_ratio(muscle_to_check.lower(), item.lower()) >=85:
                print(f"found item {item} and muscle {muscle}")
                return item, muscle

def which_sub():
    muscle_dict = get_muscles()
    muscle_message = "The muscle sub groups are ->_\n"
    for key, value in muscle_dict.items() :
        muscle_message+=f"_{key}: {value}_\n"
    return muscle_message

def get_machines():
    data = sql_fetch_existing(ALL_MACHINE,None)
    formatted_data = [row['machine_name'] for row in data]
    return formatted_data


def get_muscle_id(muscle):
    params = (muscle,)
    data = sql_fetch_existing(MUSCLE_ID,params)
    muscle_id = data[0]['muscle_id']
    group_id = data[0]['group_id']
    return muscle_id, group_id

def get_machine_id(machine):
    params = (machine,)
    data = sql_fetch_existing(MACHINE_ID,params)
    if len(data) == 0:
        return machine
    machine_id = data[0]['machine_id']
    return machine_id

def get_exercise_id(exercise):
    params = (exercise,)
    data = sql_fetch_existing(EXERCISE_ID,params)
    exercise_id = data[0]['exercise_id']
    return exercise_id

if __name__ =="__main__":
    get_machine_id("Cables")
        