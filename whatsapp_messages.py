from muscle_machine_names import MUSCLES
INTRO = """Do you want to..._\n_Find exercises for a muscle?_\n
    _Find your current lift for an exercise?_\n
    _Insert a new exercise?_\n
    _End session?"""

MUSCLE_EXAMPLE = f"""Here are some examples\nBack: {', '.join(MUSCLES['TRICEPS'])}_\n
    _Chest: {', '.join(MUSCLES['CHESTS'])}\nLegs: {', '.join(MUSCLES['LEGS'])}_\n
    _Shoulders: {', '.join(MUSCLES['SHOULDERS'])}\nBiceps: {', '.join(MUSCLES['BICEPS'])}_\n
    _Tricps: {', '.join(MUSCLES['TRICEPS'])}"""

WHICH_SUB = f"""The muscle sub groups are ->_\n
    _Back: {', '.join(MUSCLES['BACKS'])}_\n
    _Chest: {', '.join(MUSCLES['CHESTS'])}_\n_Legs: {', '.join(MUSCLES['LEGS'])}_\n
    _Shoulders: {', '.join(MUSCLES['SHOULDERS'])}_\n_Biceps: {', '.join(MUSCLES['BICEPS'])}_\n
    _Tricps: {', '.join(MUSCLES['TRICEPS'])}"""

CHECK_INPUT ="""You entered_\n
    _Exercise name :{}, machine :{}, Intensity of exercise :{}_
    _optimum level :{}, tips :{}, link :{}_\n_Muscle list :{}, Muscle group :{}"""