# Abschlussprojekt-Softwaredesign
Musikerkennung Software

Installationsanleitung:
1. Installieren Sie Git LFS auf Ihrem System. Die Installationsanweisungen finden Sie auf der
offiziellen Git LFS Webseite(https://git-lfs.github.com/)
2. Initialisieren Sie Git LFS in GitBash: ”git lfs install”
3. Installation für pydub: ffmpeg installieren -> https://phoenixnap.com/kb/ffmpeg-windows 
3. Klonen Sie das Repository: ”git clone https://github.com/xbakerman/Abschlussprojekt-Softwaredesign.git”
4. Wechseln Sie in das Verzeichnis des geklonten Repositories: ”cd Abschlussprojekt-Softwaredesign”
5. Erstellen Sie eine virtuelle Umgebung und aktivieren Sie sie: ”python3 -m venv venv”
”source venv/bin/activate” On Windows, use ”venv\Scripts\activate”
6. Installieren Sie die ben¨otigten Python-Pakete: ”pip install -r requirements.txt”
7. Um die Datenbank zu ¨offnen kann eine Extension wie ”SQLite Viewer”verwendet werden
8. Um die Software zu starten, führen Sie die Datei interface.py aus: ”streamlit run interface.py”

--------------------------------------------

Dateien für Software:
- requirements.txt
- README.md
- interface.py
- database_start.py
- Recognise.py
- Register.py
- Serialize_data.py
- my_database.db
- database.sql
- queries.py
- songs.py
- duckduckgo_integration.py
- youtube_integration.py

--------------------------------------------
Erweiterungen:
- Songerkennung via Mikrofon
- Albumcover 
- Youtube Link

--------------------------------------------
Anmerkungen:
- je lauter und näher am Mikrofon der Song abgespielt wird, desto besser wird erkannt
- In den Systemeinstellungen vom PC für Mikrofon 44100Hz einstellen!!
- Im Bericht ist eine detaillierte Beschreibung des Projekts zu finden
- Audiodatei vom hochgeladenen Song wird im "Samples" Ordner gespeichert
- recorded_audio.wav ist die aufgenommene Audiodatei vom Mikrofon (wird überschrieben)
--------------------------------------------




