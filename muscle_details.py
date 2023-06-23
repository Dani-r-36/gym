
from fuzzywuzzy import fuzz
from itertools import zip_longest


BICEPS = ["outer bi", "inner bi", "brachialis"]
TRICEPS = ["long  head", "lateral head", "medial head"]
SHOULDERS = ["middle delt", "front delts", "rear delts", "traps"]
BACKS = ["Middle lats", "lower lats", "upper back", "lower back"]
CHESTS = ["upper chest", "middle chest", "lower chest"]
LEGS = ["Quads", "hamstrings", "glutes", "calfs", "inner adductors", ' outer adductors']

def find_muscle_group(muscle): 
    for bi, tri, shou, back, chest, leg in zip_longest(BICEPS, TRICEPS, SHOULDERS, BACKS, CHESTS, LEGS, fillvalue=None):
        print(fuzz.partial_ratio(muscle, shou))
        if fuzz.partial_ratio(muscle, bi) > 75:
            return bi
        if fuzz.partial_ratio(muscle, tri) > 75:
            return tri
        if fuzz.partial_ratio(muscle, shou) > 75:
            return shou
        if fuzz.partial_ratio(muscle, back) > 75:
            return back
        if fuzz.partial_ratio(muscle, chest) > 75:
            return chest
        if fuzz.partial_ratio(muscle, leg) > 75:
            return leg
