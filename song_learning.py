import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft, signal
from scipy.ndimage import maximum_filter
from scipy.ndimage import label
from scipy.io import wavfile
from scipy.signal import spectrogram
from pydub import AudioSegment
import hashlib
from database_start import DatabaseConnector
from songs import Song

# Funktion zum Generieren von Spektrogrammen
def generate_spectrogram(audio_file_path):
    y, sr = librosa.load(audio_file_path)

    plt.figure(figsize=(12, 8))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    #plt.show()

    return np.abs(librosa.stft(y))

# Funktion zum Finden von Peaks im Spektrogramm
def find_peaks(spectrogram):
    return librosa.util.peak_pick(spectrogram, pre_max=2, post_max=2, pre_avg=5, post_avg=5, delta=0.1, num_peaks=3)

# Funktion zum Generieren von Hashes für Peaks
def generate_hashes(peaks):
    hashes = []
    for peak in peaks:
        peak_hash = hashlib.sha256(str(peak).encode()).hexdigest()
        hashes.append(peak_hash)
    return hashes

def create_constellation(audio, Fs):
    # Parameters
    window_length_seconds = 0.5
    window_length_samples = int(window_length_seconds * Fs)
    window_length_samples += window_length_samples % 2
    num_peaks = 15

    # Pad the song to divide evenly into windows
    amount_to_pad = window_length_samples - audio.size % window_length_samples

    song_input = np.pad(audio, (0, amount_to_pad))

    # Perform a short time fourier transform
    frequencies, times, stft = signal.stft(
        song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples, return_onesided=True
    )

    constellation_map = []

    for time_idx, window in enumerate(stft.T):
        # Spectrum is by default complex. 
        # We want real values only
        spectrum = abs(window)
        # Find peaks - these correspond to interesting features
        # Note the distance - want an even spread across the spectrum
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=200)

        # Only want the most prominent peaks
        # With a maximum of 15 per time slice
        n_peaks = min(num_peaks, len(peaks))
        # Get the n_peaks largest peaks from the prominences
        # This is an argpartition
        # Useful explanation: https://kanoki.org/2020/01/14/find-k-smallest-and-largest-values-and-its-indices-in-a-numpy-array/
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        for peak in peaks[largest_peaks]:
            frequency = frequencies[peak]
            constellation_map.append([time_idx, frequency])

    plt.scatter(*zip(*constellation_map))

        

    return constellation_map

def create_hashes(constellation_map, song_id=None):
    hashes = {}
    # Use this for binning - 23_000 is slighlty higher than the maximum
    # frequency that can be stored in the .wav files, 22.05 kHz
    upper_frequency = 23_000 
    frequency_bits = 10

    # Iterate the constellation
    for idx, (time, freq) in enumerate(constellation_map):
        # Iterate the next 100 pairs to produce the combinatorial hashes
        # When we produced the constellation before, it was sorted by time already
        # So this finds the next n points in time (though they might occur at the same time)
        for other_time, other_freq in constellation_map[idx : idx + 100]: 
            diff = other_time - time
            # If the time difference between the pairs is too small or large
            # ignore this set of pairs
            if diff <= 1 or diff > 10:
                continue

            # Place the frequencies (in Hz) into a 1024 bins
            freq_binned = freq / upper_frequency * (2 ** frequency_bits)
            other_freq_binned = other_freq / upper_frequency * (2 ** frequency_bits)

            # Produce a 32 bit hash
            # Use bit shifting to move the bits to the correct location
            hash = int(freq_binned) | (int(other_freq_binned) << 10) | (int(diff) << 20)
            hashes[hash] = (time, song_id)
    return hashes

# Quickly investigate some of the hashes produced


# Hauptfunktion zum Verarbeiten der Songs
def process_songs():
    # Verbindung zur Datenbank herstellen
    db_connector = DatabaseConnector()
    songs_table = db_connector.get_songs_table()

    # Alle Songs aus der Datenbank abrufen
    songs = songs_table.all()

    # Für jeden Song die Verarbeitung durchführen
    for song_data in songs:
        # Lade den Song aus der Datenbank
        song = Song.load_by_title(song_data['title'])
        
        # Lade die Audiodatei und generiere das Spektrogramm
        spectrogram = generate_spectrogram(song.file_path)

        audio, sr = librosa.load(song.file_path)
        constellation_map = create_constellation(audio, sr)
        
        hashes = create_hashes(constellation_map, song.id)
        print(hashes)

        
        song.hashes = hashes
        song.store()

# Hauptprogramm
if __name__ == "__main__":
    process_songs()
    
    