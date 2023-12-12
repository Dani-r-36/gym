import psycopg2
import psycopg2.extras 
from dotenv import dotenv_values
from sql_code import INSERT_EXERCISE_SQL,  INSERT_MACHINE, INSERT_EXERCISE_CURRENT_SQL, INSERT_CURRENT, INSERT_EXERCISE, INSERT_EXERCISE_MUSCLE, INSERT_EXERCISE_MACHINE, EXISTING_EXERCISE, EXISTING_EXERCISE_FROM_MUSCLE, FIND_EXERCISE_DETAILS, UPDATE_CURRENT_ID
from muscle_details import current_lift, num_integer

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
        machine_id = []
        print("About to insert data")
        params = (details['exercise_name'],details['exercise_name'],)
        exercise_id = int(sql_execute_fetch_one(INSERT_EXERCISE, params, "exercise_id"))
        print("Inserted exercise name")
        for id in details['muscle_list']:
            params = (exercise_id, id,)
            sql_insert_data(INSERT_EXERCISE_MUSCLE, params)
        print("Inserted exercise muscle ids")
        for machine_name in details['machine_list']:
            if num_integer(machine_name):
                machine_id.append(machine_name)
            else:
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
            print("Inserrted exercise details with current lifts")
        else:
            params = (exercise_id, details['intensity'], details['tips'], details['optimum'], details['link'],exercise_id, details['intensity'], details['tips'], details['optimum'], details['link'])
            sql_insert_data(INSERT_EXERCISE_SQL, params)
            print("Inserrted exercise details")
    except Exception as err:
        print (err)
        return error_message("Error in inserting data",'')

def lift_edit(exercise, exercise_id):
    weight, reps = current_lift(exercise)
    params = (weight, reps, weight, reps)
    current_id = sql_execute_fetch_one(INSERT_CURRENT, params, "current_id")
    print("Inserted current lift")
    params = (current_id,exercise_id)
    sql_insert_data(UPDATE_CURRENT_ID, params)
    print("Updated current_lift")

def existing_exercise(exercise_name):
    print("checking if exists")
    params = (exercise_name,)
    data = sql_fetch_existing(EXISTING_EXERCISE,params)
    print("data from existing exercise",data)
    formatted_data = []
    for row in data:
        exercise = {"exercise_name":row['exercise_name'],"exercise_id":row['exercise_id']}
        formatted_data.append(exercise)
    if len(formatted_data) == 0:
        return False
    return formatted_data



def exercise_from_muscle(muscle, group):
    print("finding exercises")
    params = (muscle, group,)
    data = sql_fetch_existing(EXISTING_EXERCISE_FROM_MUSCLE,params)
    print(data)
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
    params = (exercise,)
    data = sql_fetch_existing(FIND_EXERCISE_DETAILS, params)
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
    curs.execute(sql, params)
    print("exectued")
    data = curs.fetchall()
    conn.commit()
    curs.close()
    return data

def error_message(message,num):
    """handles all error messages"""
    return {"error": True, "Message": message, "Status_code":num}

if __name__ =="__main__":
    existing_exercise("Pull-up")