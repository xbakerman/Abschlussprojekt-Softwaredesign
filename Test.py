

from songs import songs
from database_start import DatabaseConnector
from Recognise import recognize_song

import os


song_title = "Adieu"
song_artist = "Tchami"
song_file_path = "Samples/9613057_Adieu_(Original Mix).mp3"  
song_hashes = []  

folder_path = 'Samples'





db_connector = DatabaseConnector()



audio_file_path = 'AudioTests/Audio_Test7.mp3'

recognize_song(audio_file_path, db_connector)


#hier wurden Funktionen getestet und aufgerufen.