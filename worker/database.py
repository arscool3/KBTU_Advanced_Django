import psycopg2
import datetime

INSERT_QUERY = "INSERT INTO user_song_table (user_id, song_id, time) VALUES (%s, %s, %s)"


def insert_listened(user_id: int, song_id: int):
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="password",
        host="postgres",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute(INSERT_QUERY, (user_id, song_id, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    cur.close()
    conn.close()
