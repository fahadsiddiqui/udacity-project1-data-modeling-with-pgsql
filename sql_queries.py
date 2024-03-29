# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users ; "
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS 
songplays (songplay_id serial primary key , 
start_time timestamp not null, 
user_id int not null, 
level varchar(100), 
song_id varchar(30), 
artist_id varchar(30),
session_id int not null, 
location text,
user_agent text);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS
users ( user_id int primary key ,
first_name varchar(250) not null,
last_name varchar(250),
gender char(1), 
level varchar(100) ) ;
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS
songs (song_id varchar(30) PRIMARY KEY , 
title varchar(250),
artist_id varchar(30),
year int,
duration float);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS
artists (artist_id varchar(30) PRIMARY KEY, name varchar(150),
location text, 
latitude float, 
longitude float) ;
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS
time (start_time TIMESTAMP PRIMARY KEY,
hour int, 
day int, 
week int, 
month int, 
year int, 
weekday varchar(15));
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays ( songplay_id,start_time, user_id, level, song_id,
                           artist_id, session_id, location, user_agent)
    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS
song_select = ("""
   SELECT songs.song_id, songs.artist_id
                  FROM songs
                  INNER JOIN artists
                  ON songs.artist_id=artists.artist_id
                  WHERE songs.title = %s
                  AND artists.name = %s
                  AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create,
                        song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop]
