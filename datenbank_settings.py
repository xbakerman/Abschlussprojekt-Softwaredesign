import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('datenbank.db')

# SQL-Code für Tabellenerstellung
sql_create_songs_table = """
CREATE TABLE IF NOT EXISTS Songs (
    song_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    album TEXT,
    duration INTEGER,
    file_path TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Hashes (
    hash_id INTEGER PRIMARY KEY,
    song_id INTEGER,
    hash_value TEXT NOT NULL,
    time_diff INTEGER,
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);
"""

# Cursor erstellen und SQL-Code ausführen
cur = conn.cursor()
cur.executescript(sql_create_songs_table)

# Verbindung schließen
conn.close()
