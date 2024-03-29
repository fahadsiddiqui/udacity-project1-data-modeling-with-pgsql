import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description: This function is used to populate the song and
            artist dim tables by reading the files in the
            filepath (data/song_data) to get the song and artist info.

    Parameters:
        cur: the cursor object.
        filepath: song data file path.

    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = song_data = list(
        df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])

    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude',
                           'artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description: This function is used to populate the users and
            time dim tables by reading the files in the
            filepath (data/log_data) to get the user and time info.

    Parameters:
        cur: the cursor object.
        filepath: log data file path.

    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    ts = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = [[t, t.hour, t.day, t.week, t.month, t.year, t.day_name()]
                 for t in ts]
    column_labels = ('start_time', 'hour', 'day',
                     'week', 'month', 'year', 'weekday')

    time_df = pd.DataFrame.from_records(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [pd.to_datetime(row.ts, unit='ms'), int(row.userId), row.level, songid,
                         artistid, row.sessionId,                                    row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Description: This function reads all file names in the given filepath.
            These are then iterated and passed to the respective function
            for further processing and data fetching.

    Parameters:
        cur: the cursor object.
        conn: object of the connection to the database.
        filepath: log data file path.
        func: function to continue processing

    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Description: This function connects to the database and provides the cursor,
            also starts the datas reading and processing.

    Parameters:
        None

    Returns:
        None
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
