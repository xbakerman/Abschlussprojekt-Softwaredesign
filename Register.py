import json 
import numpy as np
import librosa
from tinydb import TinyDB, Query
from scipy.signal import find_peaks
import hashlib

def load_song_data(music_database):
    with open('music_database.json') as f:
        music_database = json.load(f)
    return music_database 

def calculate_spectrogram(audio, sr):
    spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr)
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
    return spectrogram_db

def extract_fingerprints(spectrogram):
    # Konvertiere das zweidimensionale Spektrogramm in ein eindimensionales Array
    flattened_spectrogram = spectrogram.flatten()
    
    peak_threshold = np.max(flattened_spectrogram) * 0.8
    peaks, _ = find_peaks(flattened_spectrogram, height=peak_threshold)
    fingerprint = [(peak, flattened_spectrogram[peak]) for peak in peaks]
    
    return fingerprint

def hash_fingerprint(fingerprint):
    fingerprint_str = json.dumps(fingerprint, sort_keys=True)
    fingerprint_hash = hashlib.sha256(fingerprint_str.encode()).hexdigest()
    return fingerprint_hash
   


def save_song_to_database(artist, title, file):
    audio, sr = librosa.load(file, sr=None)
    spectrogram = calculate_spectrogram(audio, sr)
    fingerprints = extract_fingerprints(spectrogram)
    fingerprint_hashes = [hash_fingerprint(fp) for fp in fingerprints]

    serialized_fingerprints = [[peak, value] for peak, value in fingerprints]
    
    db = TinyDB('music_database.json')
    music_table = db.table('music', cache_size=0)
    music_table.insert({'artist': artist, 'title': title, 'fingerprints': serialized_fingerprints})