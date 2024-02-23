# Importiere die relevanten Klassen und Funktionen

from songs import Song 

import os

# Erstelle eine Instanz der Song-Klasse mit den entsprechenden Informationen zum Song
song_title = "Adieu"
song_artist = "Tchami"
song_file_path = "Samples/9613057_Adieu_(Original Mix).mp3"  # Passe den Dateipfad entsprechend an
song_hashes = []  # Du kannst die Hashes später generieren, nachdem du das Spektrogramm erstellt hast

folder_path = 'Samples'

# Erzeuge eine Instanz des Songs
new_song = Song(song_title, song_artist, song_file_path, song_hashes)

new_song.store()



loaded_song = Song.load_by_title(song_title)

# Überprüfen, ob der Song erfolgreich geladen wurde
if loaded_song:
    print("Song geladen:", loaded_song)
    # Jetzt kannst du mit dem geladenen Song weiterarbeiten, z.B. Spektrogramm generieren, Hashes berechnen, usw.
else:
    print("Song nicht gefunden.")



