import psycopg2
import psycopg2.extras 
from dotenv import dotenv_values

def get_db_connection():
    """establishes connection to database"""
    try:
        config = dotenv_values('/users/dani/Documents/anime/.env')
        connection = psycopg2.connect( user = config["DATABASE_USERNAME"], password = config["DATABASE_PASSWORD"], host = config["DATABASE_HOST"], port = config["DATABASE_PORT"], database = config["DATABASE_NAME"]) 
        return connection
    except:
        print("Error connecting to database.")

conn = get_db_connection()

def sql_insert_data(sql,params):
    """handles most sql inserts"""
    curs = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    curs.execute(sql, params)
    conn.commit()
    curs.close()

def error_message(message,num):
    """handles all error messages"""
    return {"error": True, "Message": message, "Status_code":num}
