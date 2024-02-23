from Serialize_data import Serializable
from database_start import DatabaseConnector
from tinydb import Query

class Song(Serializable):
    
    def __init__(self, title, artist, file_path, hashes) -> None:
        super().__init__(title)  # Verwende den Titel als ID
        self.title = title
        self.artist = artist
        self.file_path = file_path
        self.hashes = hashes

    @classmethod
    def get_db_connector(cls):
        return DatabaseConnector().get_songs_table()

    def store(self):
        print("Storing song...")
        super().store()

    @classmethod
    def load_by_id(cls, id):
        print("Loading song...")
        data = super().load_by_id(id)
        if data:
            return cls(data['title'], data['artist'], data['file_path'], data['hashes'])  # Lade die Daten und erstelle ein Song-Objekt
        else:
            return None
        
    @classmethod
    def load_by_title(cls, title):
        print("Loading song...")
        query = Query()
        result = cls.get_db_connector().search(query.title == title)
        if result:
            return cls(result[0]['title'], result[0]['artist'], result[0]['file_path'], result[0]['hashes'])
        else:
            return None
        
    def delete(self):
        super().delete()
        print("Song deleted.")

    def __str__(self):
        return F"Song: {self.title} by {self.artist}"

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    # Beispiel für die Verwendung der Klasse Song
    #song1 = Song("Song One", "Artist One", "/path/to/song1.mp3")
    #song2 = Song("Song Two", "Artist Two", "/path/to/song2.mp3") 
    #song3 = Song("Song Three", "Artist Three", "/path/to/song3.mp3") 
    #song1.store()
    #song2.store()
    #song3.store()

    loaded_song = Song.load_by_title("Adieu")
    if loaded_song:
        print(f"Loaded: {loaded_song}")
    else:
        print("Song not found.")

    all_songs = Song.find_all()
    for song in all_songs:
        print(song)
