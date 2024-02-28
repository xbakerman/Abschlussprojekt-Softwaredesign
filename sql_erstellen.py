import sqlite3
from database_start import DatabaseConnector

<<<<<<< HEAD


conn = sqlite3.connect('my_database.db')
conn.execute('VACUUM')
=======
# Verbindung zur SQLite-Datenbank erstellen (oder Datenbank erstellen, wenn sie nicht existiert)
conn = sqlite3.connect('my_database.db')

# Cursor-Objekt erstellen
c = conn.cursor()


# Erstelle einen Index auf der 'hash' Spalte in der 'hashes' Tabelle
c.execute("CREATE INDEX hash_index ON hashes (hash)")


    # Änderungen speichern und Verbindung schließen
conn.commit()
>>>>>>> 30b42035201db0f5eae2a0d32045468fa9214d62
conn.close()
