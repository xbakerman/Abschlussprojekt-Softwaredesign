# Importiere die relevanten Klassen und Funktionen

from songs import songs
from database_start import DatabaseConnector
from Recognise import recognize_song

import os

# Erstelle eine Instanz der Song-Klasse mit den entsprechenden Informationen zum Song
song_title = "Adieu"
song_artist = "Tchami"
song_file_path = "Samples/9613057_Adieu_(Original Mix).mp3"  # Passe den Dateipfad entsprechend an
song_hashes = []  # Du kannst die Hashes später generieren, nachdem du das Spektrogramm erstellt hast

folder_path = 'Samples'





db_connector = DatabaseConnector()


# Passe den Dateipfad entsprechend deiner Umgebung an
audio_file_path = 'AudioTests/Audio_Test7.mp3'
# Funktion aufrufen und die Audiodatei erkennen lassen
recognize_song(audio_file_path, db_connector)


