from abc import ABC, abstractmethod
from database_start import DatabaseConnector
from tinydb import Query

class Serializable(ABC):

    @abstractmethod
    def __init__(self, id):
        self.id = id
    
    @classmethod
    def find_all(cls):
        return cls.get_db_connector().all()

    @classmethod
    @abstractmethod
    def get_db_connector(cls):
        return None
    
    @classmethod
    @abstractmethod
    def load_by_id(cls, id):
        query = Query()
        result = cls.get_db_connector().search(query.id == id)
        if result:
            return result[0]
        else:
            return None

    def store(self) -> None:
        print("  Storing data...")
        query = Query()
        result = self.get_db_connector().search(query.id == self.id)

        if result:
            result = self.get_db_connector().update(self.to_dict(), doc_ids=[result[0].doc_id])
            print("  Data updated.")
        else:
            self.get_db_connector().insert(self.to_dict())
            print("  Data inserted.")

    def delete(self) -> None:
        query = Query()
        result = self.get_db_connector().remove(query.id == self.id)

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
