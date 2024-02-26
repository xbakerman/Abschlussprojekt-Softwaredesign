import os
import sqlite3

class DatabaseConnector:
    """
    Usage: DatabaseConnector().get_songs_table()
    The information about the actual database file path and the serializer objects has been abstracted away into this class
    """
    # Turns the class into a naive singleton
    # --> not thread safe and doesn't handle inheritance particularly well
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'my_database.db')
        return cls.__instance

    def get_songs_table(self):
        conn = sqlite3.connect(self.path)
        return conn.cursor()



