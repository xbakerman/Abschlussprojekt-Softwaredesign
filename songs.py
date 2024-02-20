import os
from tinydb import TinyDB, Query
from database_start import DatabaseConnector
from Serialize_data import Serializable
import librosa
import numpy as np
import hashlib


class Song(Serializable):
    def get_db_connector(self):
        return DatabaseConnector().get_songs_table()

    @classmethod
    def get_all_names(cls):
        return [song['name'] for song in Song.get_db_connector(Song)]
        return [song['title'] for song in Song.get_db_connector(Song)]

    @classmethod
    def get_all_ids(cls):
        return [song['id'] for song in Song.get_db_connector(Song)]
    def _init_(self, title, hashes) -> None:
        super()._init_(title)
        
        self.title = title
        self.hashes = hashes
 
    @classmethod
    def load_data_by_id(cls, id):
        query = Query()
        result = cls.get_db_connector(cls).search(query.id == id)
        if result:
            data = result[0]
            return cls(data['title'], data['hashes'])
        else:
            return None
    
    @classmethod
    def load_data_by_title(cls, title):
        query = Query()
        result = cls.get_db_connector(cls).search(query.title == title)
        if result:
            data = result[0]
            return cls(data['title'], data['hashes'])
        else:
            return None
        
    def __init__(self, title, artist, hashes) -> None:
        super().__init__(title)
        self.title = title
        self.artist = artist
        self.hashes = hashes
        self.spectrogram = None  # Spektrogrammattribut hinzufügen

    # Andere Methoden der Song-Klasse...

    def generate_spectrogram(self, audio_file_path):
        # Lese die Audiodatei ein
        y, sr = librosa.load(audio_file_path)

        # Berechne das Spektrogramm
        spectrogram = np.abs(librosa.stft(y))

        # Aktualisiere das Spektrogrammattribut
        self.spectrogram = spectrogram

        return spectrogram
    
    def find_peaks(self, threshold=0.1):
        if self.spectrogram is None:
            raise ValueError("Spektrogramm wurde noch nicht generiert.")

        # Hier implementiere die Logik zur Peak-Findung, z.B. mit Peakutils oder einer eigenen Methode

    def generate_hashes(self):
        if self.spectrogram is None:
            raise ValueError("Spektrogramm wurde noch nicht generiert.")

        # Finde Peaks im Spektrogramm
        peaks = self.find_peaks()

        # Erzeuge Hashes für Peaks
        hashes = []
        for peak in peaks:
            # Erzeuge einen Hashwert für jeden Peak
            peak_hash = hashlib.sha256(str(peak).encode()).hexdigest()
            hashes.append(peak_hash)

        return hashes
    
    def save_to_database(self):
        # Speichere das Lied in der Datenbank
        db = DatabaseConnector('music_database.json')
        music_table = db.get_table('music')

        # Speichere die Attribute des Songs in der Datenbank
        music_table.insert({'artist': self.artist, 'title': self.title, 'hashes': self.hashes})
        
    def _str_(self):
        return f'Song: {self.title} ({self.hashes})'
    def _repr_(self):
        return self._str_()