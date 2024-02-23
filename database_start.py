from tinydb.storages import JSONStorage
from datetime import datetime, date, time
from tinydb_serialization import Serializer, SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
import os
from tinydb import TinyDB, Query
from tinydb.table import Table

class DatabaseConnector:
    """
    Usage: DatabaseConnector().get_devices_table()
    The information about the actual database file path and the serializer objects has been abstracted away into this class
    """
    # Turns the class into a naive singleton
    # --> not thread safe and doesn't handle inheritance particularly well
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music_database.json')
        return cls.__instance

    def get_songs_table(self) -> Table:
        return TinyDB(self.path, storage=serializer).table('songs')


serializer = SerializationMiddleware(JSONStorage)

