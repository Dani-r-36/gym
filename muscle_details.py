
from fuzzywuzzy import fuzz
from itertools import zip_longest


BICEPS = ["Outer bi", "Inner bi", "Brachialis"]
TRICEPS = ["Long head", "Lateral head", "Medial head"]
SHOULDERS = ["Middle delt", "Front delts", "Rear delts", "Traps"]
BACKS = ["Middle lats", "Lower lats", "Upper back", "Lower back"]
CHESTS = ["Upper chest", "Middle chest", "Lower chest"]
LEGS = ["Quads", "Hamstrings", "Glutes", "Calfs", "Inner adductors", 'Outer adductors']

def find_muscle_group(muscle): 
    for bi, tri, shou, back, chest, leg in zip_longest(BICEPS, TRICEPS, SHOULDERS, BACKS, CHESTS, LEGS, fillvalue=None):
        if fuzz.partial_ratio(muscle, bi) > 85:
            return bi
        if fuzz.partial_ratio(muscle, tri) > 85:
            return tri
        if fuzz.partial_ratio(muscle, shou) > 85:
            return shou
        if fuzz.partial_ratio(muscle, back) > 85:
            return back
        if fuzz.partial_ratio(muscle, chest) > 85:
            return chest
        if fuzz.partial_ratio(muscle, leg) > 85:
            return leg
