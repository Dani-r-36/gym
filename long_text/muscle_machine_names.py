"""ALL muscles, machines and exercise in DB. Can add more machines and exercises"""

MUSCLES = {
    "BICEPS" : ["Outer bi", "Inner bi", "Brachialis"],
    "TRICEPS" : ["Long head", "Lateral head", "Medial head"],
    "SHOULDERS" : ["Middle delt", "Front delts", "Rear delts", "Traps"],
    "BACKS" : ["Middle lats", "Lower lats", "Upper back", "Lower back"],
    "CHESTS" : ["Upper chest", "Middle chest", "Lower chest"],
    "LEGS" : ["Quads", "Hamstrings", "Glutes", "Calves", "Inner adductors", 'Outer adductors']
}

MACHINES = ["Cables", "Dumbbells", "barbell", "bench", "squat rack", "Incline chest press machine", 
"Smith machine", "chest supported free weight row machine", "Lat pull machine", "Parallel row machine", "pull-up dip station",
"Pec fly machine", "Seated calves raise machine", "standing calves raise machine", "Leg press free weight", "Hack squat machine",
"Leg press machine", "Prone leg curl machine", "Leg extension machine", "Machine preacher curl", "Inner adductor machine",
"Outer adductor machine", "Free weight shoulder press machine"]

EXERCISE_NAME = {
    "Biceps" : ["Seated bicep curl", "Seated bicep curl and hammer curl", "Seated inclined curl", "Machine preacher curl", 
"Machine hammer curl on preacher", "Hammer rope curl", "Standing hammer curl", "Seated hammer curl", "Standing bicep curl",
"Standing ez bar curl", "Preacher curl"],

    "Triceps": ["Single extension", "Single extension far and close", "Both cable extension", "Dips",
"JM press", "Ez bar skullcrusher", "DB skullcrusher", "Single cable overhead extension", "Rope extension far and close", 
"V bar extension"],

"Shoulders": ["DB shoulder press", "Free weight machine shoulder press", "Smith machine shoulder press", "DB side raises", 
"Chest supported side raises", "Standing side raises", "Cable side raises", "Cable rear delts", "Reverse pec fly's", "DB Shrug", 
"Free weight shrug machine"],

"Backs": ["Lat pull down", "D-handle lat pull down", "Single D-handle lat pull down", "Parallel row machine", "Chest support row free weight",
"Chest support row machine", "Kneeing single lat pull", "High lat pull machine", "Chest supported T-bar", "Pull-up"],

"Chests": ["Incline chest press machine (free weight)", "Incline chest press machine", "Smith machine Incline chest press", 
"Smith machine chest press", "DB Chest press", "Incline DB chest press", "Pec fly"],

"Legs": ["Hack squat", "Barbell RDL", "DB RDL", "Barbell Squats", "Seated Calves raise", "Standing Calves raise", "Leg press machine (free weight)",
"Leg press machine", "Single leg press machine (free weight)", "Single leg press machine", "Prone leg curls", "Seated leg curls", "Leg extensions",
"Outer abductors", "Inner abductors", "Slight raised back foot split squat", "DB bulgarian split squat"]
}