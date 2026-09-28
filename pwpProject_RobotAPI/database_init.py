import sqlite3

#create and connect to sql
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

#creates sql table for login
cursor.execute("""CREATE TABLE IF NOT EXISTS USERBASE (
UserID INTEGER PRIMARY KEY AUTOINCREMENT,
Username VARCHAR(16) UNIQUE NOT NULL,
Password VARCHAR(16) NOT NULL);""")

conn.commit()
conn.close()
