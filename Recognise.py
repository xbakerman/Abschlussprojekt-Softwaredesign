import librosa
import librosa.display
from database_start import DatabaseConnector
from songs import songs
import sqlite3
from Register import create_constellation, create_hashes, record_audio
import logging




def find_best_match(hashes, db_connector):
    
    scores = score_hashes(hashes, db_connector)
    
    if not scores:
        print("Keine Übereinstimmungen gefunden.")
        return
    
    best_match = scores[0]  
    
    song_id = best_match[0]
    best_song = songs.load_by_title(song_id)

    if best_song:
        if best_match[1][1] >= 50:
            print(f"Beste Übereinstimmung: {best_song.title}, Score: {best_match[1][1]}")
            print(f"Artist: {best_song.artist}, File Path: {best_song.file_path}")
            return best_song
        else:
            print("Kein Match.")
            return None
    else:
        print("Das beste übereinstimmende Lied konnte nicht gefunden werden.")
        return None

    



def score_hashes(hashes, db_connector):
    matches_p_song = {}

    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    
    for hash, (sample_time, _) in hashes.items():

        c.execute("SELECT time, song_id FROM hashes WHERE hash = ?", (hash,))
        matching_occurrences = c.fetchall()

        for source_time, song_idx in matching_occurrences:

            if song_idx not in matches_p_song:
                matches_p_song[song_idx] = []

            matches_p_song[song_idx].append((hash, sample_time, source_time))

    scores = {}


    for song_idx, matches in matches_p_song.items():
        song_scores_offset = {}

        for hash, sample_time, source_time in matches:
            delta = abs(source_time - sample_time)

            if delta not in song_scores_offset:
                song_scores_offset[delta] = 0
            song_scores_offset[delta] += 1



        max_offset = max(song_scores_offset, key=song_scores_offset.get)
        max_score = song_scores_offset[max_offset]
        scores[song_idx] = (max_offset, max_score)

    
    scores = sorted(scores.items(), key=lambda x: x[1][1], reverse=True)

    return scores


def recognize_song(audio_file, db_connector):
    logging.info(f"Recognizing song for file: {audio_file}")
    logging.info(f"Database connection status: {db_connector}")


    
    # Lade die Audiodatei und generiere das Spektrogramm
    audio, sr = librosa.load(audio_file)
    print("Sampling rate (Abtastrate):", sr)
    
    print(f"Loaded audio of length {len(audio)}")

    constellation_map = create_constellation(audio, sr)
    print(f"Created constellation map with {len(constellation_map)} points")

    hashes = create_hashes(constellation_map, None)
    print(f"Created {len(hashes)} hashes")
    
    
    print("Finding matches...")
    
    result = find_best_match(hashes, db_connector)
    return result



def record_and_recognize():

    db_connector = DatabaseConnector()
   
    audio = record_audio("recorded_audio.wav")

    audio, sr = librosa.load("recorded_audio.wav")

    constellation_map = create_constellation(audio, sr)
    print(f"Created constellation map with {len(constellation_map)} points")

    hashes = create_hashes(constellation_map, None)
    print(f"Created {len(hashes)} hashes")

    print("Finding matches...")

    result = find_best_match(hashes, db_connector)
    return result



