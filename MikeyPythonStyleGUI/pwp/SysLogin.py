import subprocess
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from sqlcipher3 import dbapi2 as sqlite

#Make sure to install neccessary python libraries

enter_4quadgui=False

conn = sqlite3.connect('user_log.db')
conn.execute("PRAGMA key = 'super_secure_password';")
cursor = conn.cursor()

def table_exists(db_name, table_name):
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
  result=cursor.fetchone()
  return result is not None

if table_exists('user_log.db', 'userlogs'):
  print("Table already exists")
else:
  cursor.execute("""
      CREATE TABLE userlogs (
        UserID INTEGER PRIMARY KEY,
        Username varchar,
        Password varchar
      )
  """)

def save_table():
  conn.commit()
  cursor.close()
  conn.close()

#used for debugging, not intended for functionality
def extinguish_table():
  cursor.execute("DROP TABLE userlogs")

def sign_in_func():
  sign_in = tk.Tk()
  sign_in.geometry("500x500")
  sign_in.resizable(width=True, height=True)
  sign_in.title("Sign In")
  
  def show_table_func():
    cursor.execute("SELECT * FROM userlogs")
    all_table=cursor.fetchall()
    print(all_table)
  
  def create_account_func():
    sign_in.destroy()
    create_acc = tk.Tk()
    create_acc.geometry("1000x200")
    create_acc.resizable(width=False, height=False)
    create_acc.title("Create Account")
    
    def go_back_create():
      create_acc.destroy()
      sign_in_func()
    
    def username_lim(P):
      max=20
      if len(P) <= max:
        return True
      else:
        return False
    user_verify=create_acc.register(username_lim)
    
    def password_lim(P):
      max=20
      if len(P) <= max:
        return True
      else:
        return False
    password_verify=create_acc.register(password_lim)
    
    def add_new_acc():
      new_user=username.get()
      new_password=password.get()
      cursor.execute("SELECT Username FROM userlogs WHERE EXISTS (SELECT Username FROM userlogs WHERE Username=?)", (new_user,))
      is_username=cursor.fetchone()
      if is_username:
        messagebox.showinfo("Message", f"Username already in use, please enter different username")
      else:
        cursor.execute("INSERT INTO userlogs (Username, Password) VALUES (?, ?)", (new_user, new_password))
        cursor.execute("SELECT Username, Password FROM userlogs WHERE Username=? AND Password=?", (new_user, new_password,))
        result=cursor.fetchone()
        if result:
          messagebox.showinfo("Message", f"User: {result[0]} Pass: {result[1]} Now entering 4quadGUI")
          save_table()
          create_acc.update()
          subprocess.run(["python3", "4quadGUI.py"])
          quit()
        else:
          print("None")  
    
    username=StringVar()
    user_name_label=Label(create_acc, text="Enter username (Under 20 characters): ")
    user_name_label.grid(row=0, column=0)
    user_name=Entry(create_acc, textvariable=username, validate="key", validatecommand=(user_verify, '%P'))
    user_name.grid(row=0, column=1)
    
    password=StringVar()
    pass_word_label=Label(create_acc, text="Enter password (Under 20 characters): ")
    pass_word_label.grid(row=0, column=2)
    pass_word=Entry(create_acc, textvariable=password, validate="key", validatecommand=(password_verify, '%P'))
    pass_word.grid(row=0, column=3)
    
    create_account_butt=Button(create_acc, text="Create New Account", command=add_new_acc)
    create_account_butt.grid(row=1, column=0)
    
    return_create=Button(create_acc, text="Return", command=go_back_create)
    return_create.grid(row=1, column=2)
    
  def log_in_func():
    sign_in.destroy()
    log_in = tk.Tk()
    log_in.geometry("1000x200")
    log_in.resizable(width=False, height=False)
    log_in.title("Log In")
    
    def go_back_log():
      log_in.destroy()
      sign_in_func()
    
    def username_lim(P):
      max=20
      if len(P) <= max:
        return True
      else:
        return False
    user_verify = log_in.register(username_lim)
    
    def password_lim(P):
      max=20
      if len(P) <= max:
        return True
      else:
        return False
    password_verify = log_in.register(password_lim)
    
    def check_log_in():
      chosen_user=username.get()
      chosen_pass=password.get()
      cursor.execute("SELECT Username, Password FROM userlogs WHERE EXISTS (SELECT Username, Password FROM userlogs WHERE Username=? AND Password=?)", (chosen_user, chosen_pass,)) 
      valid=cursor.fetchone()
      if valid:
        messagebox.showinfo("Message", f"Entering 4quadGUI")
        save_table()
        log_in.update()
        subprocess.run(["python3", "4quadGUI.py"])
        quit()
      else:
        messagebox.showinfo("Message", f"Invalid username and/or incorrect password. Please try again or create new account.")
    
    username=StringVar()
    user_name_label=Label(log_in, text="Enter username (Under 20 characters): ")
    user_name_label.grid(row=0, column=0)
    user_name=Entry(log_in, textvariable=username, validate="key", validatecommand=(user_verify, '%P'))
    user_name.grid(row=0, column=1)
    
    password=StringVar()
    pass_word_label=Label(log_in, text="Enter password (Under 20 characters): ")
    pass_word_label.grid(row=0, column=2)
    pass_word=Entry(log_in, textvariable=password, validate="key", validatecommand=(password_verify, '%P')) 
    pass_word.grid(row=0, column=3)
    
    #def verify_user():
      #user=user_name.get()
      #print(f"Username: {user}")
      #if len(user)>20:
        #messagebox.showinfo("Message", "Username greater than 20 characters, try again")
      #else:
        #messagebox.showinfo("Message", "Valid username")
    log_in_butt=Button(log_in, text="Log in", command=check_log_in)
    log_in_butt.grid(row=1, column=0)
    
    return_log=Button(log_in, text="Return", command=go_back_log)
    return_log.grid(row=1, column=2)
  
  pls_log = Button(sign_in, text="Log in to an existing account", command=log_in_func)
  pls_log.grid(row=0, column=0)
  pls_create = Button(sign_in, text="Create new account", command=create_account_func)
  pls_create.grid(row=0, column=1)
  
  #only for debugging, not intended for functionality (change columns of buttons below when excluding and including)
  #show_table=Button(sign_in, text="Show All Accounts", command=show_table_func)
  #show_table.grid(row=0, column=2)
  #WARNING: DELETES ENTIRE TABLE. Are you sure your debugging is worth it?
  #clear_table_butt=Button(sign_in, text="Erase All Accounts", command=extinguish_table)
  #clear_table_butt.grid(row=0, column=3)
  
  quit_button=Button(sign_in, text="Exit", command=quit)
  quit_button.grid(row=0, column=2)
  
  sign_in.mainloop()

sign_in_func()

