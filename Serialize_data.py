from abc import ABC, abstractmethod
from database_start import DatabaseConnector
import os
import sqlite3
from abc import ABC, abstractmethod

class Serializable(ABC):

    @abstractmethod
    def __init__(self, id):
        self.id = id
    
    @classmethod
    def find_all(cls):
        return cls.get_db_connector().execute(f"SELECT * FROM {cls.__name__}").fetchall()

    @classmethod
    @abstractmethod
    def get_db_connector(cls):
        return sqlite3.connect('my_database.db')

    @classmethod
    @abstractmethod
    def load_by_id(cls, id):
        result = cls.get_db_connector().execute(f"SELECT * FROM {cls.__name__} WHERE id=?", (id,)).fetchone()
        if result:
            return result
        else:
            return None

    def store(self) -> None:
      print("  Storing data...")
      conn = self.get_db_connector()
      c = conn.cursor()
      result = c.execute(f"SELECT * FROM {self.__class__.__name__} WHERE id=?", (self.id,)).fetchone()
      

      if result:
          
          c.execute(f"UPDATE {self.__class__.__name__} SET title=?, artist=?, file_path=? WHERE id=?", (self.title, self.artist, self.file_path, self.id))
          print("  Data updated.")
      else:
          
          c.execute(f"INSERT INTO {self.__class__.__name__} (id, title, artist, file_path) VALUES (?, ?, ?, ?)", (self.id, self.title, self.artist, self.file_path))
          print("  Data inserted.")
      conn.commit()
      conn.close()

    def delete(self) -> None:
        conn = self.get_db_connector()
        c = conn.cursor()
        c.execute(f"DELETE FROM {self.__class__.__name__} WHERE id=?", (self.id,))
        c.execute("DELETE FROM hashes WHERE song_id=?", (self.id,))

            
        if self.file_path:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)

        conn.commit()
        conn.close()

    

    def to_dict(self, *args):
        """
        This function converts an object recursively into a dict.
        It is not necessary to understand how this function works!
        """

        if len(args) > 0:
            obj = args[0]
        else:
            obj = self

        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = self.to_dict(v)
            return data
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            data = [self.to_dict(v) for v in obj]
            return data
        elif hasattr(obj, "__dict__"):
            data = []
            for k, v in obj.__dict__.items():
                data.append((k, self.to_dict(v)))
            return dict(data)
        else:
            return obj

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass
