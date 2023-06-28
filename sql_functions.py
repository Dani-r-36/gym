import psycopg2
import psycopg2.extras 
from dotenv import dotenv_values
from sql_code import INSERT_EXERCISE_SQL, INSERT_MUSCLE_GROUP, INSERT_MUSCLE, INSERT_MACHINE, INSERT_EXERCISE_CURRENT_SQL, INSERT_CURRENT
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

def insert_new_exercise(driver, machine, intensity, optimum, tips, link, formated_muscle, muscle_group, exercise_name, user_request):
    try:
        # conn = get_db_connection()
        # curs = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        # curs.execute("Select * from group_muscle;", "")
        # data =curs.fetchall()
        # curs.close()
        # print(data)
        params = (muscle_group, muscle_group,)
        group_id = sql_execute_fetch_one(INSERT_MUSCLE_GROUP, params, "group_id")
        params = (formated_muscle, group_id, formated_muscle, group_id,)
        muscle_id = sql_execute_fetch_one(INSERT_MUSCLE, params, "muscle_id")
        params = (machine, muscle_id, machine, muscle_id,)
        exercise_id = sql_execute_fetch_one(INSERT_MACHINE, params, "exercise_id")
        params = (exercise_id, intensity, tips, optimum, link,exercise_id, intensity, tips, optimum, link)
        if user_request == "Yes" or user_request == "yes":
            weight, reps = current_lift(driver, exercise_name)
            params = (weight, reps, weight, reps)
            current_id = sql_execute_fetch_one(INSERT_CURRENT, params, "current_id")
            params = (exercise_id, current_id, intensity, tips, optimum, link,exercise_id, current_id, intensity, tips, optimum, link)
            exercise_details_id = sql_execute_fetch_one(INSERT_EXERCISE_CURRENT_SQL, params, "exercise_details_id")
        else:
            params = (exercise_id, intensity, tips, optimum, link,exercise_id, intensity, tips, optimum, link)
            exercise_details_id = sql_execute_fetch_one(INSERT_EXERCISE_SQL, params, "exercise_details_id")
    except Exception as err:
        print (err)
        return error_message("Error in inserting data",'')

def sql_execute_fetch_one(sql,params,id):
    """handles most sql executes"""
    conn = get_db_connection()
    curs = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    curs.execute(sql, params)
    data = curs.fetchone()[id]
    curs.close()
    return data

def sql_insert_data(sql,params):
    """handles most sql inserts"""
    conn = get_db_connection()
    curs = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    curs.execute(sql, params)
    conn.commit()
    curs.close()

def error_message(message,num):
    """handles all error messages"""
    return {"error": True, "Message": message, "Status_code":num}
