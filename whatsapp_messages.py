from muscle_machine_names import MUSCLES
INTRO = """
    Do you want to...\nFind exercises for a muscle?\n
    Find your current lift for an exercise?\n
    Insert a new exercise?\n
    End session?"""

MUSCLE_EXAMPLE = f"""
    Here are some examples\nBack: {', '.join(MUSCLES['TRICEPS'])}\n
    Chest: {', '.join(MUSCLES['CHESTS'])}\nLegs: {', '.join(MUSCLES['LEGS'])}\n
    Shoulders: {', '.join(MUSCLES['SHOULDERS'])}\nBiceps: {', '.join(MUSCLES['BICEPS'])}\n
    Tricps: {', '.join(MUSCLES['TRICEPS'])}
    """

WHICH_SUB = f"""
    Please enter which of the following sub-muscle group the exercise belongs to\n
    Back: {', '.join(MUSCLES['BACKS'])}\n
    Chest: {', '.join(MUSCLES['CHESTS'])}\nLegs: {', '.join(MUSCLES['LEGS'])}\n
    Shoulders: {', '.join(MUSCLES['SHOULDERS'])}\nBiceps: {', '.join(MUSCLES['BICEPS'])}\n
    Tricps: {', '.join(MUSCLES['TRICEPS'])}
    """