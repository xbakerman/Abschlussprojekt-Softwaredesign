import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft, signal
import hashlib
from database_start import DatabaseConnector
from songs import songs
from scipy.io.wavfile import read
import sqlite3
from Register import create_constellation, create_hashes
import logging
import sounddevice as sd
from pydub import AudioSegment
import io
import tempfile




def find_best_match(hashes, db_connector):
    
    scores = score_hashes_against_database(hashes, db_connector)
    
    if not scores:
        print("Keine Übereinstimmungen gefunden.")
        return
    
    best_match = scores[0]  
    
    song_id = best_match[0]
    best_song = songs.load_by_title(song_id)

    if best_song:
        print(f"Beste Übereinstimmung: {best_song.title}, Score: {best_match[1][1]}")
        print(f"Artist: {best_song.artist}, File Path: {best_song.file_path}")
        return best_song
    else:
        print("Das beste übereinstimmende Lied konnte nicht gefunden werden.")
        return None


def score_hashes_against_database(hashes, db_connector):
    matches_per_song = {}
    conn = sqlite3.connect('my_database.db')

    c = conn.cursor()
    
    for hash, (sample_time, _) in hashes.items():
        c.execute("SELECT time, song_id FROM hashes WHERE hash = ?", (hash,))
        matching_occurrences = c.fetchall()

        for source_time, song_index in matching_occurrences:

            if song_index not in matches_per_song:
                matches_per_song[song_index] = []

            matches_per_song[song_index].append((hash, sample_time, source_time))

    scores = {}
    for song_index, matches in matches_per_song.items():
        song_scores_by_offset = {}

        for hash, sample_time, source_time in matches:
            delta = abs(source_time - sample_time)

            if delta not in song_scores_by_offset:
                song_scores_by_offset[delta] = 0
            song_scores_by_offset[delta] += 1

        max_offset = max(song_scores_by_offset, key=song_scores_by_offset.get)
        max_score = song_scores_by_offset[max_offset]
        scores[song_index] = (max_offset, max_score)

    
    scores = sorted(scores.items(), key=lambda x: x[1][1], reverse=True)

    return scores

def recognize_song(audio_file, db_connector):
    logging.info(f"Recognizing song for file: {audio_file}")
    logging.info(f"Database connection status: {db_connector}")


    
    # Lade die Audiodatei und generiere das Spektrogramm
    audio, sr = librosa.load(audio_file)
    print(f"Loaded audio of length {len(audio)}")

    constellation_map = create_constellation(audio, sr)
    print(f"Created constellation map with {len(constellation_map)} points")

    hashes = create_hashes(constellation_map, None)
    print(f"Created {len(hashes)} hashes")
    
    
    print("Finding matches...")
    
    # Gibt die Top-Übereinstimmungen aus
    

    result = find_best_match(hashes, db_connector)
    return result

