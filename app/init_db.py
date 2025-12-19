import sqlite3
import os

DB_FILE = 'database.db'

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

connection = sqlite3.connect(DB_FILE)

with open('app/schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
