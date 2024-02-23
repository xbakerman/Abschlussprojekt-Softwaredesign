import os
from tinydb import Query
from database_start import DatabaseConnector

def find_songs() -> list:
    """Find all songs in the database."""
    # Define the database connector
    db_connector = DatabaseConnector().get_songs_table()
    # Create a query object
    SongQuery = Query()
    # Search the database for all songs
    result = db_connector.all()
    
    # The result is a list of dictionaries, we only want the song titles
    if result:
        result = [x["title"] for x in result]
    
    return result

if __name__ == "__main__":
    print(find_songs())
