import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import librosa
from pydub import AudioSegment
import os
from scipy.ndimage import maximum_filter
import json

audio_filename = 'Samples/9613057_Adieu_(Original Mix).mp3'
audio = AudioSegment.from_file(audio_filename)
audio.export('Samples/9613057_Adieu_(Original Mix).wav', format='wav')

#y, sr = librosa.load('Samples/9613057_Adieu_(Original Mix).wav')
#D = np.abs(librosa.stft(y))
#plt.figure()
#librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), y_axis='log', x_axis='time')
#plt.title('Power spectrogram')
#plt.colorbar(format='%+2.0f dB')
#plt.tight_layout()
#plt.show()

with open('music_database.json') as f:
    music_database = json.load(f)

database = music_database['samples']

for samples in database:
    print("ID:", samples['id'])
    print("Name:", samples['name'])
    print("Artist:", samples['artist'])
    print("Path:", samples['file_path']) 






