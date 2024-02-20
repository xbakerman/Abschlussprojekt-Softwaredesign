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
    def _new_(cls):
        if cls.__instance is None:
            cls._instance = super().new_(cls)
            cls._instance.path = os.path.join(os.path.dirname(os.path.abspath(file_)), 'music_database.json')
        return cls.__instance
    
    def get_songs_table(self) -> Table:
        return TinyDB(self.__instance.path, storage=serializer).table('songs')
    
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = TinyDB(db_path)

    def get_table(self, table_name):
        return self.db.table(table_name)


serializer = SerializationMiddleware(JSONStorage)