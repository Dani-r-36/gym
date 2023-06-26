
from fuzzywuzzy import fuzz
from itertools import zip_longest

MUSCLES = {
    "BICEPS" : ["Outer bi", "Inner bi", "Brachialis"],
    "TRICEPS" : ["Long head", "Lateral head", "Medial head"],
    "SHOULDERS" : ["Middle delt", "Front delts", "Rear delts", "Traps"],
    "BACKS" : ["Middle lats", "Lower lats", "Upper back", "Lower back"],
    "CHESTS" : ["Upper chest", "Middle chest", "Lower chest"],
    "LEGS" : ["Quads", "Hamstrings", "Glutes", "Calfs", "Inner adductors", 'Outer adductors']
}

def find_muscle_group(muscle_to_check): 
    for muscle, muscle_list in MUSCLES.items():
        for item in muscle_list:
            if fuzz.partial_ratio(muscle_to_check.lower(), item.lower()) >=85:
                return item, muscle
