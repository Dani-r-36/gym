INSERT_MUSCLE_GROUP = f"""
WITH ins AS (
    INSERT INTO group_muscle (muscle_group)
    VALUES (%s)
    ON CONFLICT DO NOTHING
    RETURNING group_id
)
SELECT group_id FROM ins
UNION ALL
SELECT group_id FROM group_muscle
WHERE muscle_group = %s;
"""

INSERT_MUSCLE = f"""
WITH ins AS (
    INSERT INTO muscle (muscle_name, group_id)
    VALUES (%s,%s)
    ON CONFLICT DO NOTHING
    RETURNING muscle_id
)
SELECT muscle_id FROM ins
UNION ALL
SELECT muscle_id FROM muscle
WHERE muscle_name = %s
    AND group_id = %s;
"""

INSERT_EXERCISE = f"""
WITH ins AS (
    INSERT INTO exercise (exercise_name)
    VALUES (%s)
    ON CONFLICT DO NOTHING
    RETURNING exercise_id
)
SELECT exercise_id FROM ins
UNION ALL
SELECT exercise_id FROM exercise
WHERE exercise_name = %s;
"""

INSERT_EXERCISE_MUSCLE = f"""
INSERT INTO exercise_muscle (exercise_id, muscle_id)
VALUES (%s,%s)
ON CONFLICT DO NOTHING;
"""

INSERT_MACHINE = f"""
WITH ins AS (
    INSERT INTO machine (machine_name)
    VALUES (%s)
    ON CONFLICT DO NOTHING
    RETURNING machine_id
)
SELECT machine_id FROM ins
UNION ALL
SELECT machine_id FROM machine
WHERE machine_name = %s;
"""
INSERT_EXERCISE_MACHINE = f"""
INSERT INTO exercise_machine (exercise_id, machine_id)
VALUES (%s,%s)
ON CONFLICT DO NOTHING;
"""

INSERT_EXERCISE_SQL=f"""
WITH ins AS (
    INSERT INTO exercise_details (exercise_id, intensity, tips, optimum_level, picture_video_link)
    VALUES (%s,%s,%s,%s,%s)
    ON CONFLICT DO NOTHING
    RETURNING exercise_details_id
)
SELECT exercise_details_id FROM ins
UNION ALL
SELECT exercise_details_id FROM exercise_details
WHERE exercise_id = %s
    AND intensity = %s
    AND tips = %s
    AND optimum_level = %s
    AND picture_video_link = %s;
"""

INSERT_CURRENT = f"""
WITH ins AS (
    INSERT INTO current_lift (max_working_weight, max_reps)
    VALUES (%s,%s)
    ON CONFLICT DO NOTHING
    RETURNING current_id
)
SELECT current_id FROM ins
UNION ALL
SELECT current_id FROM current_lift
WHERE max_working_weight = %s
    AND max_reps = %s;
"""

INSERT_EXERCISE_CURRENT_SQL = """
WITH ins AS (
    INSERT INTO exercise_details (exercise_id, current_id, intensity, tips, optimum_level, picture_video_link)
    VALUES (%s,%s,%s,%s,%s,%s)
    ON CONFLICT DO NOTHING
    RETURNING exercise_details_id
)
SELECT exercise_details_id FROM ins
UNION ALL
SELECT exercise_details_id FROM exercise_details
WHERE exercise_id = %s
    AND current_id = %s
    AND intensity = %s
    AND tips = %s
    AND optimum_level = %s
    AND picture_video_link = %s;
"""


EXISTING_EXERCISE = """
SELECT exercise_name
FROM exercise
WHERE similarity(exercise_name, %s) > 0.5;
"""