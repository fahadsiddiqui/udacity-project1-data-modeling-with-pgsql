# Data Modeling with Postgres

## Project Overview

A start-up called Sparkify wants to analyze the data they've been
collecting on songs and user activity on their new
music streaming app. The analytics team is particularly interested in understanding what songs users are listening to.
Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

## Project Description

This project creates data model in Postgres to store `songplays` analytical data. An ETL pipeline is part of the project
to load songs/logs data from `data` directory and populate tables after applying transformations in Python.

## Data Model (Star Schema)

### Fact Table

**songplays** - Main data table used for analytical queries about song plays.

- songplay_id BIGSERIAL PRIMARY KEY,  _(uniquely indentifies a song play)_
- start_time TIMESTAMP REFERENCES time(start_time),  _(start time of user song play, FK from `time` table)_
- user_id INT REFERENCES users(user_id),  _(FK from `users` table, identifying a user)_
- level VARCHAR(100),   _(level of a user)_
- song_id VARCHAR(30) REFERENCES songs(song_id),  _(FK from `songs` table, identifying a song)_
- artist_id VARCHAR(30) REFERENCES artists(artist_id),  _(FK from `artists` table, identifying an artist)_
- session_id INT NOT NULL,  _(user session id from log file)_
- location TEXT,  _(location of user from log file)_
- user_agent TEXT  _(user agent string from log file)_

`songplay_id` is chosen as Primary Key as it uniquely identifies a records. Other columns contain duplicate values.

### Dimension Tables

**users**  - users information from log files

- user_id SERIAL PRIMARY KEY,
- first_name VARCHAR(250) NOT NULL,
- last_name VARCHAR(250),
- gender CHAR(1),
- level VARCHAR(100)

`user_id` is chosen as Primary Key because it unique indentifies a user. Other columns may contain duplicate values.

**songs**  - songs information from songs json files

- song_id VARCHAR(30) PRIMARY KEY,
- title VARCHAR(250) NOT NULL,
- artist_id VARCHAR(30),
- year SMALLINT NOT NULL DEFAULT 0,
- duration FLOAT NOT NULL DEFAULT 0

`song_id` is chosen as Primary Key.

**artists**  - artists information from songs json files

- artist_id VARCHAR(30) PRIMARY KEY,
- name VARCHAR(150) NOT NULL,
- location TEXT,
- latitude VARCHAR(100),
- longitude VARCHAR(100)

`artist_id` is chosen as Primary Key.

**time**  - timestamps from log files broken down into units

- start_time TIMESTAMP PRIMARY KEY,
- hour SMALLINT,
- day SMALLINT,
- week SMALLINT,
- month SMALLINT,
- year SMALLINT,
- weekday VARCHAR(15)

`start_time` is selected as primary key as it is a unique value.

## Description of Quries

### Drop/Create Tables

These queries are pretty straight forward and create/drop tables.

### Insert Statements

There are seperate insert quries for each table. These are upsert queries rather than simple insert statements. The
reason behind this choice is to ignore conflicting insert satements (on primary key columns). However, for the users
table insert, it will update the level of the user if there is a conflict. `EXCLUDED` table is used in
the `ON CONFLICT UPDATE` part of the `UPSERT` statement to get the new value being inserted.

### Find Songs Query

It selects `song_id` and `artist_id` by JOINing `songs` and `artists` tables ON `artist_id`. The problem this query is
solving is that there is no information about `artist_id` and `song_id` in the log file so we had to JOIN these two
tables to get the required information (to insert in songplays table) based on `title`, `artist_name` and `duration`.

## Description of Project Files/Directories

`data`: contains data about songs and logs of song plays.

`test.ipynb`: displays the first few rows of each table for verification.

`create_tables.py`: drops and creates tables. Run this file to reset tables before running ETL scripts.

`etl.ipynb`: reads and processes a single file from `song_data` and `log_data` and loads the data into tables.

`etl.py`: reads and processes all files from `song_data` and `log_data` and loads them into tables.

`sql_queries.py`: contains all sql queries, and is imported into the last three files above.

`README.md`: contains discussion about the project.

## Author

[Fahad Siddiqui](https://github.com/fahadsiddiqui)
