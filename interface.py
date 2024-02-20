import streamlit as st
from tinydb import TinyDB, Query
from PIL import Image
import time
from io import BytesIO
from songs import Song
from database_start import DatabaseConnector
import os
import librosa


# Logo einbinden
logo_path = "Logo.jpg"  # Passe den Pfad zu deinem Logo an
logo_image = Image.open(logo_path)

# Willkommensnachricht
welcome_message = "Welcome to SoundWizard, your music recognition tool"

# Aufteilung der Seite in zwei Spalten (Logo und Text nebeneinander)
col1, col2 = st.columns([1, 2])

# In der ersten Spalte das Logo platzieren
col1.image(logo_image, use_column_width=False, width=200)  # Passe die Breite nach Bedarf an

# In der zweiten Spalte die Willkommensnachricht platzieren
col2.title(welcome_message)


class MusicApp:
    def __init__(self):
        self.initialize_ui()
        self.db_connector = DatabaseConnector('music_database.json')
        self.initialize_ui()
        self.create_temp_directory()

    def create_temp_directory(self):
        # Überprüfe, ob das temporäre Verzeichnis existiert, andernfalls erstelle es
        if not os.path.exists('temp'):
            os.makedirs('temp')

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

    def learn_workflow(self):
        st.session_state["state"] = "Learn Music"
        st.header("Learn Music")
        # Hier kannst du die UI-Elemente für das Einlernen von Musikstücken hinzufügen
        artist = st.text_input("Artist:")
        title = st.text_input("Title:")
        file = st.file_uploader("Upload file", type=["mp3", "wav"])

        if st.button("Add"):
            if artist and title and file:
                # Überprüfe, ob eine Datei hochgeladen wurde
                if isinstance(file, BytesIO):
                    # Speichere die hochgeladene Datei temporär
                    temp_file_path = os.path.join("temp", file.name)
                    with open(temp_file_path, "wb") as f:
                        f.write(file.read())

                    # Erstelle eine Instanz des Songs
                    song = Song(artist, title, hashes=[])

                    # Berechne das Spektrogramm und extrahiere die Fingerabdrücke
                    song.generate_hashes()

                    # Speichere den Song in der Datenbank
                    song.save_to_database()

                    # Gib eine Erfolgsmeldung aus
                    st.success(f"Music '{title}' by '{artist}' has been successfully learned.")
                else:
                    st.error("Please upload an audio file.")

                # Lösche die temporäre Datei
                os.remove(temp_file_path)

                # Lösche die Eingabefelder
                st.text_input("Artist:", value="")
                st.text_input("Title:", value="")
                st.empty()  # Leerzeile einfügen, um das Drag-and-Drop-Menü nach dem Hochladen zu aktualisieren

    def recognize_workflow(self):
        st.session_state["state"] = "Identify Music"
        st.header("Identify Music")
        # Hier kannst du die UI-Elemente für die Identifikation von Musikstücken hinzufügen
        file_to_recognize = st.file_uploader("Upload file", type=["mp3", "wav"])

        if st.button("Identify"):
            if file_to_recognize:
                # Führe die Identifikation durch und zeige das Ergebnis an (Annahme: Die Funktion ist in der Musikerkennung implementiert)
                # result = MusicRecognizer.recognize_music(file_to_recognize)
                # st.success(f"Music identified as '{result}'.")
                st.success("Music has been identified. (Function not yet implemented)")

                # Füge den "Listen"-Button nur im "Identify Music"-Modus hinzu
                if st.button("Listen"):
                    self.listen_workflow()

    def listen_workflow(self):
        st.header("Listen to Music")

        # Video während des Hörvorgangs
        video_path = "listening.mp4"  # Passe den Pfad zu deinem Video an

        # IPython Video-Element mit Breite und Autoplay
        #video = Video(video_path, embed=True, width=400)

        # Anzeige des Videos
        #st.markdown(f"### Video Preview\n{video._repr_html_()}", unsafe_allow_html=True)

        # Hier kannst du die UI-Elemente für das Lauschen von Musikstücken hinzufügen
        st.info("Listening... Please play the music to be recognized.")

        # Simuliere das Zuhören für einige Zeit (in diesem Beispiel 30 Sekunden)
        time.sleep(30)

        # Nach dem Hören den erkannten Song anzeigen (Annahme: Die Funktion ist in der Musikerkennung implementiert)
        st.success("Music has been identified. (Function not yet implemented)")

if __name__ == "__main__":
    app = MusicApp()
