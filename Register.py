import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy import fft, signal
from database_start import DatabaseConnector
from songs import songs
import sounddevice as sd
import pyaudio
import wave


def create_Fingerprints(audio, Fs):
    
    window_l_s = 0.5                    #Fensterlänge in Sekunden
    window_l_sa = int(window_l_s * Fs)  #Fensterlänge in Samples
    window_l_sa += window_l_sa % 2      #Fensterlänge auf gerade Anzahl an Samples runden
    n_peaks = 15                        #Anzahl der Peaks, die pro Fenster berücksichtigt werden

    
    amount_to_pad = window_l_sa - audio.size % window_l_sa
    song_input = np.pad(audio, (0, amount_to_pad))
    freq, times, stft = signal.stft(song_input, Fs, nperseg=window_l_sa, nfft=window_l_sa, return_onesided=True)

    constellation_map = []

    for time_index, window in enumerate(stft.T):
        spectrum = abs(window)
        peak_indices, _ = signal.find_peaks(spectrum, prominence=0, distance=200)
        n_peaks = min(15, len(peak_indices))
        largest_peaks = np.argpartition(spectrum[peak_indices], -n_peaks)[-n_peaks:]

        for peak_index in peak_indices[largest_peaks]:
            frequency = freq[peak_index]
            constellation_map.append([time_index, frequency])                       #Hinzufügen der Peaks zum Constellation Map

    plt.scatter(*zip(*constellation_map))
    plt.xlabel('Time Index')
    plt.ylabel('Frequency')
    plt.title('Constellation Map')
    
    return constellation_map



def create_hashes(constellation_map, song_id=None):
    hashes = {}

    high_frequency = 23_000 
    freq_bits = 10

    for idx, (time, freq) in enumerate(constellation_map):
        for other_idx in range(idx + 1, min(idx + 76, len(constellation_map))):
            other_t, other_freq = constellation_map[other_idx]
            dif = other_t - time
            
            if dif <= 1 or dif > 10:
                if freq > high_frequency * 0.8:  
                    freq_binned = freq / high_frequency * (2 ** freq_bits)
                    other_freq_binned = other_freq / high_frequency * (2 ** freq_bits)
                    hash_value = int(freq_binned) | (int(other_freq_binned) << 10) | (int(dif) << 20)
                    hashes[hash_value] = (time, song_id)
                continue

            freq_binned = freq / high_frequency * (2 ** freq_bits)
            other_freq_binned = other_freq / high_frequency * (2 ** freq_bits)
            hash_value = int(freq_binned) | (int(other_freq_binned) << 10) | (int(dif) << 20)
            hashes[hash_value] = (time, song_id)

    return hashes




def process_song(artist, title, audio_file_path, hashes, db_connector):
    
    song = songs.load_by_title(title)
    
    
    if song:
        
        audio, sr = librosa.load(audio_file_path)
        constellation_map = create_Fingerprints(audio, sr)

        hashes = create_hashes(constellation_map, song.id)
        print(f"Created {len(hashes)} hashes")
        
        songs.store_hashes(hashes, song.id)
    else:
        print("Song not found in the database.")



def process_uploaded_song(artist, title, audio_file):
    # Verbindung zur Datenbank herstellen
    db_connector = DatabaseConnector()
    
    
    audio_file_path = f"Samples/{title}.mp3"
    with open(audio_file_path, "wb") as f:
        f.write(audio_file.read())
    
    audio, sr = librosa.load(audio_file_path)
    constellation_map = create_Fingerprints(audio, sr)

    hashes = create_hashes(constellation_map)
    print(f"Created {len(hashes)} hashes")

    process_song(artist, title, audio_file_path, hashes, db_connector)


def record_audio_simple(duration, fs):
    duration = 10  
    fs = 22050  

    
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.float32)
    sd.wait()  
    
    return audio


def record_audio(filename=None):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    print("* recording")

    frames = []
    

    for i in range(0, int(44100 / 1024 * 13)):
        data = stream.read(1024)
        frames.append(data)
        

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    if filename is not None:
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

    return np.hstack(frames)


