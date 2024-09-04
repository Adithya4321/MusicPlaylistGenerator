import pandas as pd
import mysql.connector

# Load the dataset
df = pd.read_csv(r'C:\Users\adith\Downloads\Projects\Music Playlist Generator\DataSet_Music\tcc_ceds_music.csv')

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Ensure you have the correct password or update it
    database="music_playlist_db",
    charset='utf8'
)

cursor = mydb.cursor()

# Create table in MySQL if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS music_data (
    Unnamed_0 INT,
    artist_name VARCHAR(255),
    track_name VARCHAR(255),
    release_date INT,
    genre VARCHAR(50),
    lyrics TEXT,
    len INT,
    dating FLOAT,
    violence FLOAT,
    world_life FLOAT,
    night_time FLOAT,
    shake_the_audience FLOAT,
    family_gospel FLOAT,
    romantic FLOAT,
    communication FLOAT,
    obscene FLOAT,
    music FLOAT,
    movement_places FLOAT,
    light_visual_perceptions FLOAT,
    family_spiritual FLOAT,
    like_girls FLOAT,
    sadness FLOAT,
    feelings FLOAT,
    danceability FLOAT,
    loudness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    valence FLOAT,
    energy FLOAT,
    topic VARCHAR(255),
    age FLOAT
)
""")

# Insert data into the table
sql = """
INSERT INTO music_data (Unnamed_0, artist_name, track_name, release_date, genre, lyrics, len, dating, violence, world_life, night_time, shake_the_audience, family_gospel, romantic, communication, obscene, music, movement_places, light_visual_perceptions, family_spiritual, like_girls, sadness, feelings, danceability, loudness, acousticness, instrumentalness, valence, energy, topic, age)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Check DataFrame columns and ensure they match
print(f"DataFrame Columns: {df.columns.tolist()}")
print(f"Number of DataFrame Columns: {len(df.columns)}")

# Insert data into the table
for i, row in df.iterrows():
    try:
        cursor.execute(sql, tuple(row))
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print(f"Row data: {tuple(row)}")

# Commit the transaction
mydb.commit()

# Close the connection
cursor.close()
mydb.close()
