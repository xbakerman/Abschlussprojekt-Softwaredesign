import sqlite3
from database_start import DatabaseConnector



conn = sqlite3.connect('my_database.db')
conn.execute('VACUUM')
conn.close()



#hier wurden Befehle ausgeführt um die Datenbank zu bearbeiten.