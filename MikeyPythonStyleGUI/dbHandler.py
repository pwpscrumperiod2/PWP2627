import sqlite3
import hashlib

#Creates the conn and cursor neccessary for some of these functions to, well, function
conn = sqlite3.connect('user_log.db')
cursor = conn.cursor()

#Checks if the table inputted exists
def table_exists(db_name, table_name, cursor):
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
  result=cursor.fetchone()
  return result is not None

#Checks if user_log.db exists, and creates it if it doesn't
def check_if_exists():
  if table_exists('user_log.db', 'userlogs', cursor):
    print("Table already exists")
  else:
    cursor.execute("""
        CREATE TABLE userlogs (
          UserID INTEGER PRIMARY KEY,
          Username varchar,
          Password varchar
        )
    """)

#Encrypts the input data using hash
def encrypt_data(input):
  return hashlib.sha256(input.encode()).hexdigest()

#saves changes to the table
def save_table(conn, cursor):
  conn.commit()
  cursor.close()
  conn.close()
