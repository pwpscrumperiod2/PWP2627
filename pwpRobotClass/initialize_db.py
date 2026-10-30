#import database management library
import sqlite3
from pathlib import Path

#create and connect to sql
conn = sqlite3.connect(Path(__file__).with_name("users.db"))
cursor = conn.cursor()

#creates sql table for login
cursor.execute("""CREATE TABLE IF NOT EXISTS USERBASE (
UserID INTEGER PRIMARY KEY AUTOINCREMENT,
Username VARCHAR(16) UNIQUE NOT NULL,
Password VARCHAR(16) NOT NULL);""")

#closes database
conn.commit()
conn.close()
