CREATE TABLE IF NOT EXISTS hashes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    song_id TEXT NOT NULL,
    hash_value TEXT NOT NULL,
    time_diff INTEGER NOT NULL
);