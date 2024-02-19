import streamlit as st
from tinydb import TinyDB, Query
from PIL import Image
import time
from IPython.display import Video

# TinyDB-Verbindung
db = TinyDB('music_database.json')
music_table = db.table('music')

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
                # Füge die Informationen zur Datenbank hinzu (Annahme: Die Funktion ist in der Musikerkennung implementiert)
                # MusicRecognizer.learn_music(artist, title, file)
                st.success(f"Music '{title}' by '{artist}' has been successfully learned.")

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
        video = Video(video_path, embed=True, width=400)

        # Anzeige des Videos
        st.markdown(f"### Video Preview\n{video._repr_html_()}", unsafe_allow_html=True)

        # Hier kannst du die UI-Elemente für das Lauschen von Musikstücken hinzufügen
        st.info("Listening... Please play the music to be recognized.")

        # Simuliere das Zuhören für einige Zeit (in diesem Beispiel 30 Sekunden)
        time.sleep(30)

        # Nach dem Hören den erkannten Song anzeigen (Annahme: Die Funktion ist in der Musikerkennung implementiert)
        st.success("Music has been identified. (Function not yet implemented)")

if __name__ == "__main__":
    app = MusicApp()
