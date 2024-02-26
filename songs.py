import sqlite3
from Serialize_data import Serializable

class songs(Serializable):
    
    def __init__(self, id, title, artist, file_path) -> None:
        super().__init__(id)  # Verwende den Titel als ID
        self.title = title
        self.artist = artist
        self.file_path = file_path
        #self.hashes = hashes

    @classmethod
    def get_db_connector(cls):
        return sqlite3.connect('my_database.db')

    def store(self):
        print("Storing song...")
        super().store()
        

    @classmethod
    def load_by_id(cls, id):
        print("Loading song...")
        data = super().load_by_id(id)
        if data:
            return cls(*data)  # Lade die Daten und erstelle ein Song-Objekt
        else:
            return None
        
    @classmethod
    def load_by_title(cls, title):
        print("Loading song...")
        conn = cls.get_db_connector()
        c = conn.cursor()
        result = c.execute("SELECT id, title, artist, file_path FROM songs WHERE title=?", (title,)).fetchone()
        if result:
            return cls(*result)
        else:
            return None
        
    def store_hashes(hashes, song_id):
        conn = sqlite3.connect('my_database.db')
        c = conn.cursor()

        print(type(hashes))

        for hash, (time, _) in hashes.items():
            c.execute("INSERT INTO hashes (song_id, hash, time) VALUES (?, ?, ?)", (song_id, hash, time))

        conn.commit()
        conn.close()
        
    def delete(self):
        super().delete()
        print("Song deleted.")

    def __str__(self):
        return F"Song: {self.title} by {self.artist}"

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    # Beispiel für die Verwendung der Klasse Song
    #
    song1 = songs('3', 'Adieu', 'Tchami', 'Samples/9613057_Adieu_(Original Mix).mp3')
    #song2 = songs('4', 'I Love Rock n Roll', 'Joan Jett', "Samples/I love Rock'n'Roll.mp3") 
    #song3 = songs('5', 'Never Be Like You', 'JFlume', "Samples/Never Be Like You.mp3") 
    #song1.delete()
    #song2.delete()
    #song3.delete()
#
    ##song1.delete()
#
    #loaded_song = songs.load_by_title("103")
#
    ## Überprüfen Sie, ob der Song korrekt geladen wurde
    #if loaded_song:
    #    print(f"Loaded: {loaded_song}")
    #else:
    #    print("Song not found.")