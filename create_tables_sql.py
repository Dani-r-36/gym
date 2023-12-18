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
	exercise_name VARCHAR(200) not null,
	primary key (exercise_id)
);

create table if not exists machine(
	machine_id INT generated always as identity,
	machine_name VARCHAR(100) not null,
    primary key (machine_id)
);

create table if not exists current_lift(
	current_id INT generated always as identity,
	max_working_weight FLOAT not null,
	max_reps VARCHAR(5) not null,
	primary key (current_id)
);

create table if not exists exercise_details(
	exercise_details_id INT generated always as identity,
	exercise_id INT not null,
	current_id INT,
	intensity INT not null,
	tips VARCHAR(200) not null,
	optimum_level INT not null,
	picture_video_link VARCHAR(300) not null,
	primary key (exercise_details_id),
	foreign key (exercise_id) references exercise(exercise_id),
	foreign key (current_id) references current_lift(current_id)
);

create table if not exists exercise_muscle (
	exercise_muscle_id INT generated always as identity,
	exercise_id INT not null,
	muscle_id INT not null,
	primary key (exercise_muscle_id),
	foreign key (exercise_id) references exercise(exercise_id),
	foreign key (muscle_id) references muscle(muscle_id)
);

create table if not exists exercise_machine (
	exercise_machine_id INT generated always as identity,
	exercise_id INT not null,
	machine_id INT not null,
	primary key (exercise_machine_id),
	foreign key (exercise_id) references exercise(exercise_id),
	foreign key (machine_id) references machine(machine_id)
);


"""