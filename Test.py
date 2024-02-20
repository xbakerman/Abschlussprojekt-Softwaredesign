import librosa
import numpy as np
import hashlib
import sqlite3

# Funktion zum Erstellen des Fingerabdrucks und des Hash
def create_fingerprint(audio_file):
    # Lade das Audio
    y, sr = librosa.load(audio_file)
    # Erstelle den Chromagramm-Fingerabdruck
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    fingerprint = np.mean(chroma, axis=1)  # Mittelwert über Zeitachse
    # Erstelle einen Hash aus dem Fingerabdruck
    fingerprint_hash = hashlib.sha1(fingerprint).hexdigest()
    return fingerprint_hash

# Funktion zum Speichern des Fingerabdrucks in der Datenbank
def save_to_database(fingerprint_hash, audio_file):
    conn = sqlite3.connect('audio_fingerprints.db')
    c = conn.cursor()
    # Erstelle die Tabelle, falls sie noch nicht existiert
    c.execute('''CREATE TABLE IF NOT EXISTS fingerprints
                 (fingerprint_hash TEXT PRIMARY KEY, audio_file TEXT)''')
    # Füge den Fingerabdruck und die Datei zur Datenbank hinzu
    c.execute("INSERT INTO fingerprints (fingerprint_hash, audio_file) VALUES (?, ?)", (fingerprint_hash, audio_file))
    conn.commit()
    conn.close()

# Beispielaufruf
audio_file = 'Samples/The Kills - 103.mp3'
fingerprint_hash = create_fingerprint(audio_file)
save_to_database(fingerprint_hash, audio_file)
