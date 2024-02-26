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
from tinydb import Query
import sqlite3



def generate_spectrogram(audio_file_path):
    y, sr = librosa.load(audio_file_path)

    plt.figure(figsize=(12, 8))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    #plt.show()

    return np.abs(librosa.stft(y))


def find_peaks(spectrogram):
    return librosa.util.peak_pick(spectrogram, pre_max=2, post_max=2, pre_avg=5, post_avg=5, delta=0.1, num_peaks=3)


def generate_hashes(peaks):
    hashes = []
    for peak in peaks:
        peak_hash = hashlib.sha256(str(peak).encode()).hexdigest()
        hashes.append(peak_hash)
    return hashes

def create_constellation(audio, Fs):
    
    window_length_seconds = 0.5
    window_length_samples = int(window_length_seconds * Fs)
    window_length_samples += window_length_samples % 2
    num_peaks = 15

    
    amount_to_pad = window_length_samples - audio.size % window_length_samples

    song_input = np.pad(audio, (0, amount_to_pad))

    
    frequencies, times, stft = signal.stft(
        song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples, return_onesided=True
    )

    constellation_map = []

    for time_idx, window in enumerate(stft.T):
        
        spectrum = abs(window)
        
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=200)

        
        n_peaks = min(num_peaks, len(peaks))
        
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        for peak in peaks[largest_peaks]:
            frequency = frequencies[peak]
            constellation_map.append([time_idx, frequency])

    plt.scatter(*zip(*constellation_map))
    return constellation_map

def create_hashes(constellation_map, song_id=None):
    hashes = {}

    upper_frequency = 23_000 
    frequency_bits = 10

   
    for idx, (time, freq) in enumerate(constellation_map):
        
        for other_time, other_freq in constellation_map[idx : idx + 25]: 
            diff = other_time - time
            
            if diff <= 1 or diff > 10:
                continue

            
            freq_binned = freq / upper_frequency * (2 ** frequency_bits)
            other_freq_binned = other_freq / upper_frequency * (2 ** frequency_bits)

            hash = int(freq_binned) | (int(other_freq_binned) << 10) | (int(diff) << 20)
            hashes[hash] = (time, song_id)
    return hashes



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
    else:
        print("Das beste übereinstimmende Lied konnte nicht gefunden werden.")


def score_hashes_against_database(hashes, db_connector):
    matches_per_song = {}
    conn = sqlite3.connect('my_database.db')

    # Cursor-Objekt erstellen
    c = conn.cursor()
    print("Scoring hashes...")



    for hash, (sample_time, _) in hashes.items():
        c.execute("SELECT time, song_id FROM hashes WHERE hash = ?", (hash,))
        matching_occurences = c.fetchall()

        for source_time, song_index in matching_occurences:
            if song_index not in matches_per_song:
                matches_per_song[song_index] = []
            matches_per_song[song_index].append((hash, sample_time, source_time))

        scores = {}
        for song_index, matches in matches_per_song.items():
            song_scores_by_offset = {}
            for hash, sample_time, source_time in matches:
                delta = source_time - sample_time
                if delta not in song_scores_by_offset:
                    song_scores_by_offset[delta] = 0
                song_scores_by_offset[delta] += 1
            max = (0, 0)
            for offset, score in song_scores_by_offset.items():
                if score > max[1]:
                    max = (offset, score)

            scores[song_index] = max
        # Sort the scores for the user
        scores = list(sorted(scores.items(), key=lambda x: x[1][1], reverse=True)) 

    return scores

def recognize_song(audio_file, db_connector):
    # Lade die Audiodatei und generiere das Spektrogramm
    audio, sr = librosa.load(audio_file)
    print(f"Loaded audio of length {len(audio)}")
    constellation_map = create_constellation(audio, sr)
    print(f"Created constellation map with {len(constellation_map)} points")
    hashes = create_hashes(constellation_map, None)
    print(f"Created {len(hashes)} hashes")
    
    
    print("Finding matches...")
    
    # Gibt die Top-Übereinstimmungen aus
    find_best_match(hashes, db_connector)

# Hauptfunktion zum Verarbeiten der Songs
def process_song(artist, title, audio_file_path, hashes, db_connector):
    # Laden des Songs aus der Datenbank anhand des Titels
    song = songs.load_by_title(title)
    
    # Überprüfen, ob der Song gefunden wurde
    if song:
        # Generiere das Spektrogramm für den Song
        spectrogram = generate_spectrogram(audio_file_path)

        # Lade den Audioinhalt des Songs
        audio, sr = librosa.load(audio_file_path)
        
        # Erstelle die Sternenkarte für den Song
        constellation_map = create_constellation(audio, sr)
        
        # Erzeuge Hashes für den Song
        hashes = create_hashes(constellation_map, song.id)
        
        # Speichere die Hashes in der Datenbank
        songs.store_hashes(hashes, song.id)
    else:
        print("Song not found in the database.")

def process_uploaded_song(artist, title, audio_file):
    # Verbindung zur Datenbank herstellen
    db_connector = DatabaseConnector()
    
    # Speichere den hochgeladenen Song in einem temporären Verzeichnis
    audio_file_path = f"Samples/{title}.mp3"
    with open(audio_file_path, "wb") as f:
        f.write(audio_file.read())
    
    # Generiere das Spektrogramm und verarbeite den Song
    spectrogram = generate_spectrogram(audio_file_path)
    audio, sr = librosa.load(audio_file_path)
    constellation_map = create_constellation(audio, sr)
    hashes = create_hashes(constellation_map)
    process_song(artist, title, audio_file_path, hashes, db_connector)

# Hauptprogramm
if __name__ == "__main__":
    print("Running main program...")
    #process_songs()

    #print_top_five('Samples/Never Be Like You.mp3')
    #db_connector = DatabaseConnector()

    # Verbindung zur Datenbank herstellen
    
    db_connector = DatabaseConnector()
    songs_table = db_connector.get_songs_table()

    

    # Passe den Dateipfad entsprechend deiner Umgebung an
    audio_file_path = 'AudioTests/Audio_Test5.mp3'

    # Funktion aufrufen und die Audiodatei erkennen lassen
    recognize_song(audio_file_path, db_connector)
    
    
