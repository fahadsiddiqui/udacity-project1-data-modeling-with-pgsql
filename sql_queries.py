# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = (""" CREATE TABLE songplays (
    songplay_id BIGSERIAL PRIMARY KEY,
    start_time TIMESTAMP REFERENCES time(start_time),
    user_id INT REFERENCES users(user_id),
    level VARCHAR(100),
    song_id VARCHAR(30) REFERENCES songs(song_id),
    artist_id VARCHAR(30) REFERENCES artists(artist_id),
    session_id INT NOT NULL,
    location TEXT,
    user_agent TEXT
)
""")

user_table_create = (""" CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(250) NOT NULL,
    last_name VARCHAR(250),
    gender CHAR(1),
    level VARCHAR(100)
)
""")

song_table_create = (""" CREATE TABLE songs (
    song_id VARCHAR(30) PRIMARY KEY,
    title VARCHAR(250) NOT NULL,
    artist_id VARCHAR(30),
    year SMALLINT NOT NULL DEFAULT 0,
    duration FLOAT NOT NULL DEFAULT 0
)
""")

artist_table_create = (""" CREATE TABLE artists (
    artist_id VARCHAR(30) PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location TEXT,
    latitude VARCHAR(100),
    longitude VARCHAR(100)
)
""")

time_table_create = (""" CREATE TABLE time (
    start_time TIMESTAMP PRIMARY KEY,
    hour SMALLINT,
    day SMALLINT,
    week SMALLINT,
    month SMALLINT,
    year SMALLINT,
    weekday VARCHAR(15)
)
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays
    (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (songplay_id) DO NOTHING
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = ("""
    SELECT s.song_id, a.artist_id
    FROM songs s
    INNER JOIN artists a ON s.artist_id = a.artist_id
    WHERE s.title = %s
    AND a.name = %s
    AND s.duration = %s
""")

# QUERY LISTS

create_table_queries = reversed(
    [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create])
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
