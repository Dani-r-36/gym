from whatsapp import connect_whatsapp, send_message, last_message, wait_refresh, send_and_wait
from muscle_details import find_muscle_group, MUSCLES
import time
from fuzzywuzzy import fuzz
from selenium.webdriver.common.by import By

def start_sess(driver):
    print("running")
    time.sleep(5)
    # message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
    message_elements = driver.find_elements(By.CSS_SELECTOR, "div.message-out")
    time.sleep(5)
    last_message_element = message_elements[-1]
    # Extract the text content of each message
    message_text = last_message_element.text
    message = message_text.strip().split("\n")
    message = message[0]
    print (message)
    if message == "sess" or message == "Sess":
        record_sess(driver)
        # print(message_text)

def record_sess(driver):
    print("running sess")
    user_choice = intro_sess(driver)
    # user_choice = last_message(driver)
    print(f"they said {user_choice}")
    choice(driver, user_choice)

def intro_sess(driver):
    intro = """
    Do you want to...\nFind exercises for a muscle?\n
    Find your current lift for an exercise?\n
    Insert a new exercise?"""
    returned_message = send_and_wait(driver, intro)
    time.sleep(2)
    return returned_message
    
def choice(driver, user_choice):
    if fuzz.partial_ratio(user_choice, "Find exercises for a muscle") > 70:
        find_exercise(driver)
    # if fuzz.partial_ratio(user_choice, "Find current lift") > 70:
    #     find_current_list(driver)
    if fuzz.partial_ratio(user_choice, "Insert new exercise") > 70:
        insert_new_exercise(driver)
        print("about to call insert")
        wait = input("Press Enter to continue.")
    
def check_muscle(driver):
    muscle = last_message(driver)
    print(f"they said {muscle}")
    formated_muscle, muscle_group = find_muscle_group(muscle)
    return formated_muscle, muscle_group

def find_exercise(driver):
    message = f"""
    Here are some examples\nBack: {', '.join(MUSCLES['TRICEPS'])}\n
    Chest: {', '.join(MUSCLES['CHESTS'])}\nLegs: {', '.join(MUSCLES['LEGS'])}\n
    Shoulders: {', '.join(MUSCLES['SHOULDERS'])}\nBiceps: {', '.join(MUSCLES['BICEPS'])}\n
    Tricps: {', '.join(MUSCLES['TRICEPS'])}
    """
    send_message(driver, message)
    time.sleep(15)
    wait_refresh(driver, message)
    formated_muscle, muscle_group = check_muscle(driver)
    message = f"I'll look up your exercises for {formated_muscle} which is part of the {muscle_group} group"
    send_message(driver, message)
    #need to search for exercises but first need to insert them

def insert_new_exercise(driver):
    try:
        get_new_exercise_details(driver)
        for index, anime in enumerate(anime_titles):
            # print(anime["anime"], anime['position'], start_id[index], end_id[index], show_type_id[index], anime['eps'], anime['score'])
            sql_insert_data("""INSERT INTO animes (anime, start_date_id, end_date_id, show_type_id, episodes, score)
            VALUES (%s, %s, %s, %s, %s, %s);""",[anime["anime"], start_id[index], end_id[index], show_type_id[index], anime['eps'], anime['score']])
    except Exception as err:
        print (err)
        return error_message("Error in inserting data",'')
    
def get_new_exercise_details(driver):
    #before running need to return all exercises to make sure not already there
    message = f"""
    Please enter which of the following sub-muscle group the exercise belongs to\n
    Back: {', '.join(MUSCLES['TRICEPS'])}\n
    Chest: {', '.join(MUSCLES['CHESTS'])}\nLegs: {', '.join(MUSCLES['LEGS'])}\n
    Shoulders: {', '.join(MUSCLES['SHOULDERS'])}\nBiceps: {', '.join(MUSCLES['BICEPS'])}\n
    Tricps: {', '.join(MUSCLES['TRICEPS'])}
    """
    temp = send_and_wait(driver, message)
    formated_muscle, muscle_group = check_muscle(driver)
    message = "Please now answer all the questions in regards to the exercise"
    temp = send_and_wait(driver, message)
    message = "Please enter the machine/equipment required\nSuch as Lat pull down, Barbell, Seated parallel row machine, Dumbbells"
    machine = send_and_wait(driver, message)
    message = "What is the intensity of the exercise?\n 1 being not intense and 3 being very intense"
    intensity = send_and_wait(driver, message)
    message = "What is the optimum level of the exercise?\n 1 being not optimum and 3 being very optimum"
    optimum = send_and_wait(driver, message)
    message = "What are some tips for the exercise?"
    tips = send_and_wait(driver, message)
    message = "Please enter a link to a picture of video for the exercise\n you have 20 seconds"
    send_message(driver, message)
    wait_refresh(driver, message)
    time.sleep(20)
    link = last_message(driver)
    print(f"machine is {machine}, intensity is {intensity}, optimum is {optimum}, tips: {tips}, link: {link}")

if __name__ == "__main__":
    driver = connect_whatsapp()
    send_message(driver, "Started your tracker")
    while True:
        wait_refresh(driver, "Started your tracker")
        print("out of it ")
        start_sess(driver)