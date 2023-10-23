import psycopg2
import psycopg2.extras 
from dotenv import dotenv_values
from sql_code import INSERT_EXERCISE_SQL, INSERT_MUSCLE_GROUP, INSERT_MUSCLE, INSERT_MACHINE, INSERT_EXERCISE_CURRENT_SQL, INSERT_CURRENT, INSERT_EXERCISE, INSERT_EXERCISE_MUSCLE, INSERT_EXERCISE_MACHINE, EXISTING_EXERCISE, EXISTING_EXERCISE_FROM_MUSCLE, FIND_EXERCISE_DETAILS
from muscle_details import current_lift

def get_db_connection():
    """establishes connection to database"""
    try:
        config = dotenv_values('.env')
        connection = psycopg2.connect( user = config["DATABASE_USERNAME"], password = config["DATABASE_PASSWORD"], host = config["DATABASE_HOST"], port = config["DATABASE_PORT"], database = config["DATABASE_NAME"]) 
        return connection
    except:
        print("Error connecting to database.")

conn = get_db_connection()

def insert_new_exercise(details, user_request):
    try:
        i = 0
        j = 0
        muscle_id = []
        machine_id = []
        print("About to insert data")
        params = (details['muscle_group'], details['muscle_group'],)
        group_id = sql_execute_fetch_one(INSERT_MUSCLE_GROUP, params, "group_id")
        print("Inserted group muscle")
        for formated_muscle in details['muscle_list']:
            params = (formated_muscle, group_id, formated_muscle, group_id,)
            muscle_id.append(int(sql_execute_fetch_one(INSERT_MUSCLE, params, "muscle_id")))
        print("Inserted sub muscles")
        params = (details['exercise_name'],details['exercise_name'],)
        exercise_id = int(sql_execute_fetch_one(INSERT_EXERCISE, params, "exercise_id"))
        print("Inserted exercise name")
        for id in muscle_id:
            params = (exercise_id, id,)
            sql_insert_data(INSERT_EXERCISE_MUSCLE, params)
        print("Inserted exercise muscle ids")
        for machine_name in details['machine_list']:
            params = (machine_name, machine_name,)
            machine_id.append(int(sql_execute_fetch_one(INSERT_MACHINE, params, "machine_id")))
        print("Inserted machine")
        for mach_id in machine_id:
            params = (exercise_id, mach_id,)
            sql_insert_data(INSERT_EXERCISE_MACHINE, params)
        print("Inserted exercise machine ids")
        if user_request == "Yes" or user_request == "yes":
            weight, reps = current_lift(details['exercise_name'])
            params = (weight, reps, weight, reps)
            current_id = sql_execute_fetch_one(INSERT_CURRENT, params, "current_id")
            print("Inserted current lift")
            params = (exercise_id, current_id, details['intensity'], details['tips'], details['optimum'], details['link'],exercise_id, current_id, details['intensity'], details['tips'], details['optimum'], details['link'])
            sql_insert_data(INSERT_EXERCISE_CURRENT_SQL, params)
            print("Inserrted exercise details")
        else:
            params = (exercise_id, details['intensity'], details['tips'], details['optimum'], details['link'],exercise_id, details['intensity'], details['tips'], details['optimum'], details['link'])
            sql_insert_data(INSERT_EXERCISE_SQL, params)
            print("Inserrted exercise details")
    except Exception as err:
        print (err)
        return error_message("Error in inserting data",'')

def existing_exercise(exercise_name):
    print("checking if exists")
    params = (exercise_name,)
    data = sql_fetch_existing(EXISTING_EXERCISE,params)
    formatted_data = [row['exercise_name'] for row in data]
    if len(formatted_data) == 0:
        return False
    return formatted_data

def exercise_from_muscle(muscle, group):
    print("finding exercises")
    params = (muscle, group,)
    data = sql_fetch_existing(EXISTING_EXERCISE_FROM_MUSCLE,params)
    formatted_data = [row['exercise_name'] for row in data]
    if len(formatted_data) == 0:
        return False
    return formatted_data

def all_exercises():
    print("getting all exercises")
    data = sql_fetch_existing("SELECT exercise_name FROM exercise;", None)
    formatted_data = [row['exercise_name'] for row in data]
    if len(formatted_data) == 0:
        return False
    return formatted_data

def find_exercise_details(exercise):
    print(f"finding all details for exercise {exercise}")
    data = sql_fetch_existing(FIND_EXERCISE_DETAILS, exercise)
    if len(data) == 0:
        return False
    return data

def sql_execute_fetch_one(sql,params,id):
    """handles most sql executes"""
    conn = get_db_connection()
    curs = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    curs.execute(sql, params)
    data = curs.fetchone()[id]
    conn.commit()
    curs.close()
    return data

def sql_insert_data(sql,params):
    """handles most sql inserts"""
    conn = get_db_connection()
    curs = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    curs.execute(sql, params)
    conn.commit()
    curs.close()

def sql_fetch_existing(sql, params):
    conn = get_db_connection()
    curs = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    print(sql)
    print(params)
    curs.execute(sql, params)
    print("exectued")
    data = curs.fetchall()
    conn.commit()
    curs.close()
    return data

def error_message(message,num):
    """handles all error messages"""
    return {"error": True, "Message": message, "Status_code":num}
