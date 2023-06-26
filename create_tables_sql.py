TABLES = """
create table if not exists group_muscle(
	group_id INT generated always as identity,
	muscle_group VARCHAR(50) not null,
	primary key (group_id)
);

create table if not exists muscle(
	muscle_id INT generated always as identity,
	muscle VARCHAR(50) not null,
	group_id INT not null,
	primary key (muscle_id),
	foreign key (group_id) references group_muscle(group_id)
);

create table if not exists exercise(
	exercise_id INT generated always as identity,
	exercise_machine VARCHAR(100) not null,
	muscle_id INT not null,
	primary key (exercise_id),
	foreign key (muscle_id) references muscle(muscle_id)
);

create table if not exists current_lift(
	current_id INT generated always as identity,
	max_working_weight VARCHAR(10) not null,
	max_reps INT not null,
	primary key (current_id)
);

create table if not exists exercise_details(
	exercise_details_id INT generated always as identity,
	exercise_id INT not null,
	current_id INT,
	intensity VARCHAR(20) not null,
	tips VARCHAR(200) not null,
	optimum_level VARCHAR(20) not null,
	picture_video_link VARCHAR(50) not null,
	primary key (exercise_details_id),
	foreign key (exercise_id) references exercise(exercise_id),
	foreign key (current_id) references current_lift(current_id)
);"""