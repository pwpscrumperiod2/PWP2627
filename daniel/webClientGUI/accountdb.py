#import database management library
import sqlite3
from tkinter import messagebox
#import hashing library
import hashlib


#function to has the user data
def hash_data(inputText):
    return hashlib.sha256(inputText.encode()).hexdigest()

#create and connect to sql
def check_account(userChoice, e1, e2):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    if userChoice == 1:
        #login to account
        #check if the username is in the list of every saved username
        if hash_data(e1.get()) in [username[0] for username in cursor.execute("SELECT Username from USERBASE")]:
            #username is valid
            #get the password saved for this username and compare it
            query = "SELECT Password from USERBASE WHERE Username = ?"
            params = [hash_data(e1.get())]
            if hash_data(e2.get()) in [password[0] for password in cursor.execute(query, params)]:
                messagebox.showinfo("Notification", "Successfully Logged In")
                # ends this window
                return True
            else:
                messagebox.showinfo("Notification", "Wrong Password")
        else:
            messagebox.showinfo("Notification", "Invalid username")


    if userChoice == 2:
        #create account
        cursor.execute("SELECT Username from USERBASE")
        #check if the username is already taken
        if hash_data(e1.get()) in [username[0] for username in cursor.execute("SELECT Username from USERBASE")]:
            #username already in use
            messagebox.showinfo("Notification", "Username already used, use a different one")
        else:
            #username unused
            #add the new username and password to the database
            cursor.execute("SELECT * FROM USERBASE")
            query = "INSERT INTO USERBASE (Username, Password) VALUES (?,?)"
            params = (hash_data(e1.get()), hash_data(e2.get()))
            cursor.execute(query, params)
            messagebox.showinfo("Notification", "Successfully created account")


    #save changes and exit out of sql
    conn.commit()
    conn.close()