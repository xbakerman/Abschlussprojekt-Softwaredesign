import streamlit as st
from tinydb import TinyDB, Query
from PIL import Image
import time
from io import BytesIO
from songs import songs
from database_start import DatabaseConnector
import os
import librosa
from IPython.display import Video
from Register import process_uploaded_song
from streamlit_option_menu import option_menu
from Recognise import recognize_song 
import tempfile
import sqlite3
import soundfile as sf
import io
from scipy.io import wavfile


# Logo einbinden
logo_path = "Logo.jpg"  # Passe den Pfad zu deinem Logo an
logo_image = Image.open(logo_path)
result = None

# Willkommensnachricht
welcome_message = "Welcome to SoundWizard, your music recognition tool"

# Aufteilung der Seite in zwei Spalten (Logo und Text nebeneinander)
col1, col2 = st.columns([1, 2])

# In der ersten Spalte das Logo platzieren
col1.image(logo_image, use_column_width=False, width=200)  # Passe die Breite nach Bedarf an

# In der zweiten Spalte die Willkommensnachricht platzieren
col2.title(welcome_message)

def add_song_to_database(artist, title, audio_file):
    # Verbindung zur Datenbank herstellen
    db_connector = DatabaseConnector()
    songs_table = db_connector.get_songs_table()

    # Song in die Datenbank einfügen
    new_song = songs(id=title, artist=artist, title=title, file_path=None)  # Dateipfad vorübergehend als None setzen
    new_song.store()

    # Dateiinhalt des Audio-Uploaders lesen
    audio_content = audio_file.read()

    # Dateipfad für den Song erstellen und Audioinhalt speichern
    file_path = f"Samples/{title}.mp3"  # Beispiel-Pfad, anpassen nach Bedarf
    with open(file_path, "wb") as f:
        f.write(audio_content)

    # Dateipfad in der Datenbank aktualisieren
    new_song.file_path = file_path
    new_song.store()

def recognize_song_id(file_path, db_connector):
    # Erkenne den Song und gib das Ergebnis zurück
    return recognize_song(file_path, db_connector)

def __init__(self):
    self.initialize_ui()

def initialize_ui(self):
    st.header("Music Recognition")
    # Überprüfen, ob "state" in st.session_state existiert, wenn nicht, initialisieren
    if "state" not in st.session_state:
        st.session_state["state"] = "Learn Music"
    # Wechseln zwischen "Musikstücke einlernen" und "Musikstücke identifizieren"
    option = st.radio("Choose an option:", ["Learn Music", "Identify Music"])
    if option == "Learn Music":
        self.learn_workflow()
    elif option == "Identify Music":
        self.recognize_workflow()
    # Hier kannst du weitere UI-Elemente hinzufügen
def learn_workflow():
    st.session_state["state"] = "Learn Music"
    st.header("Learn Music")
    # Hier kannst du die UI-Elemente für das Einlernen von Musikstücken hinzufügen
    artist = st.text_input("Artist:")
    title = st.text_input("Title:")
    audio_file = st.file_uploader("Upload file", type=["mp3", "wav"])
    if artist and title and audio_file:
    # Überprüfen, ob eine Datei hochgeladen wurde
        if isinstance(audio_file, BytesIO):
            # Button zum Hinzufügen des Songs
            if st.button("Add"):
                # Song zur Datenbank hinzufügen
                add_song_to_database(artist, title, audio_file)
                st.success("Song added successfully!")
        else:
            st.error("Please upload an audio file.")
             # Verarbeitung der Songs auslösen
    if st.button("Process Song"):
                process_uploaded_song(artist, title, audio_file)
                st.success("Song processed successfully!")   



def recognize_workflow():
    global result
    st.header("Identify Music")

    with st.container():
        selected2 = option_menu(None, ["Via Upload", "Via Microphone"], 
        icons=['house', 'cloud-upload', "list-task", 'gear'], 
        menu_icon="cast", default_index=0, orientation="horizontal")

    if selected2 == "Via Upload":
    # Hier kannst du die UI-Elemente für die Identifikation von Musikstücken hinzufügen
        file_to_recognize = st.file_uploader("Upload file", type=["mp3", "wav"])

        if st.button("Identify"):
            with st.spinner("Processing..."):
                if file_to_recognize and isinstance(file_to_recognize, BytesIO):
                    #st.write("File uploaded successfully.")

                    file_to_recognize.seek(0)  # Setze den Dateizeiger auf den Anfang der Datei

                    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                        # Schreibe den Inhalt der hochgeladenen Datei in die temporäre Datei
                        tmp.write(file_to_recognize.read())
                        tmp_file_name = tmp.name
                    #st.write(f"Temporary file created: {tmp_file_name}")
                    # Öffne die temporäre Datei und zeige ihren Inhalt an
                    with open(tmp_file_name, "rb") as f:
                        content = f.read()
                        st.audio(content, format='audio/mp3')

                    try:
                        db_connector = sqlite3.connect('my_database.db') # Stelle die Verbindung zur Datenbank her
                    except Exception as e:
                        st.error(f"Failed to connect to the database: {e}")
                        return

                    # Führe die Erkennungsfunktion durch und zeige das Ergebnis an
                    result = recognize_song_id(tmp_file_name, db_connector)
                    print(result)

                    # Zeige das Ergebnis an, wenn es vorhanden ist
                    if result:
                        st.success(f"Music identified as '{result.title}' from '{result.artist}'.")

                        #st.audio(result.file_path, format='audio/mp3')
                    else:
                        st.error("No match found.")


    elif selected2 == "Via Microphone":
        if st.button("Start Recording"):
            db_connector = sqlite3.connect('my_database.db')  # Stelle die Verbindung zur Datenbank her



            with st.spinner("Processing..."):
                result, audio = recognize_song_via_mic()
                st.audio(audio, format='audio/wav')                            # Übergebe den Dateipfad der temporären Datei an deine Funktion

            if result:
                st.success(f"Music identified as '{result.title}'.")
                st.write(f"Artist: {result.artist}")
                st.audio(result.file_path, format='audio/mp3')
            else:
                st.error("No match found.")

with st.container():
    selected2 = option_menu(None, ["Register", "Recognise"], 
    icons=['bi bi-plus-circle', 'bi bi-database', "list-task", 'gear'], 
    menu_icon="cast", default_index=0, orientation="horizontal")

if __name__ == "__main__":
    if selected2 == "Register":
        learn_workflow()

    elif selected2 == "Recognise":
        recognize_workflow()
   
