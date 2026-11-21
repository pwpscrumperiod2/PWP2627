import subprocess
import sqlite3
import tkinter as tk
import dbHandler
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

#This variable gets checked in main in order to enter the quadGUI
enter_4quadgui=False

#Sets up the connection and cursor for user_log.db
conn = sqlite3.connect('user_log.db')
cursor = conn.cursor()

#Checks if user_log.db exists. If not, creates it
dbHandler.check_if_exists()

#This is the initial GUI the user if shown on launch.
def sign_in_func():
  sign_in = tk.Tk()
  sign_in.geometry("500x500")
  sign_in.resizable(width=True, height=True)
  sign_in.title("Sign In")
  
  #Closes the initial GUI and opens a new one which allows the user to create a new account
  def create_account_func():
    sign_in.destroy()
    create_acc = tk.Tk()
    create_acc.geometry("1000x200")
    create_acc.resizable(width=False, height=False)
    create_acc.title("Create Account")
    
    #Brings user back to initial GUI
    def go_back_create():
      create_acc.destroy()
      sign_in_func()
    
    #Prevents user from entering a username greater than 20 characters
    def username_lim(P):
      max=20
      if len(P) <= max:
        return True
      else:
        return False
    user_verify=create_acc.register(username_lim)
    
    #Prevents user from entering a password greater than 20 characters
    def password_lim(P):
      max=20
      if len(P) <= max:
        return True
      else:
        return False
    password_verify=create_acc.register(password_lim)
    
    #Takes user username and password and checks if username already exists. If username already exists, asks user to enter different username.
    #If username does not exist yet, adds username and password to user_log.db, whilst encrypting the data using hash
    #Then it destroys the current GUI and sets enter_4quadgui to True
    def add_new_acc():
      global enter_4quadgui
      new_user=dbHandler.encrypt_data(username.get())
      new_password=dbHandler.encrypt_data(password.get())
      cursor.execute("SELECT Username FROM userlogs WHERE EXISTS (SELECT Username FROM userlogs WHERE Username=?)", (new_user,))
      is_username=cursor.fetchone()
      if is_username:
        messagebox.showinfo("Message", f"Username already in use, please enter different username")
      else:
        cursor.execute("INSERT INTO userlogs (Username, Password) VALUES (?, ?)", (new_user, new_password))
        cursor.execute("SELECT Username, Password FROM userlogs WHERE Username=? AND Password=?", (new_user, new_password,))
        result=cursor.fetchone()
        if result:
          messagebox.showinfo("Message", f"User: {username.get()} Pass: {password.get()} Now entering 4quadGUI")
          dbHandler.save_table(conn, cursor)
          enter_4quadgui = True
          create_acc.destroy()
        else:
          print("None")  
    
    #Creates the Label and Entry box for the username
    username=StringVar()
    user_name_label=Label(create_acc, text="Enter username (Under 20 characters): ")
    user_name_label.grid(row=0, column=0)
    user_name=Entry(create_acc, textvariable=username, validate="key", validatecommand=(user_verify, '%P'))
    user_name.grid(row=0, column=1)
    
    #Creates the Label and Entry box for the password
    password=StringVar()
    pass_word_label=Label(create_acc, text="Enter password (Under 20 characters): ")
    pass_word_label.grid(row=0, column=2)
    pass_word=Entry(create_acc, textvariable=password, validate="key", validatecommand=(password_verify, '%P'))
    pass_word.grid(row=0, column=3)
    
    #Creates the button to initiate the add_new_acc function
    create_account_butt=Button(create_acc, text="Create New Account", command=add_new_acc)
    create_account_butt.grid(row=1, column=0)
    
    #Creates the button to allow the user to return to the initial GUI
    return_create=Button(create_acc, text="Return", command=go_back_create)
    return_create.grid(row=1, column=2)
    
  #destroys the initial GUI and creates the log in GUI
  def log_in_func():
    sign_in.destroy()
    log_in = tk.Tk()
    log_in.geometry("1000x200")
    log_in.resizable(width=False, height=False)
    log_in.title("Log In")
    
    #Destroys the log in GUI and runs sign_in_func
    def go_back_log():
      log_in.destroy()
      sign_in_func()
    
    #Limits the user to 20 characters for the username
    def username_lim(P):
      max=20
      if len(P) <= max:
        return True
      else:
        return False
    user_verify = log_in.register(username_lim)
    
    #Limits the user to 20 characters for the password
    def password_lim(P):
      max=20
      if len(P) <= max:
        return True
      else:
        return False
    password_verify = log_in.register(password_lim)
    
    #Checks the username and password entered to see if they exist in user_log.db
    #If the username and password exist, sets enter_4quadgui to True, and then destroys the log in GUI
    def check_log_in():
      global enter_4quadgui
      chosen_user=dbHandler.encrypt_data(username.get())
      chosen_pass=dbHandler.encrypt_data(password.get())
      cursor.execute("SELECT Username, Password FROM userlogs WHERE EXISTS (SELECT Username, Password FROM userlogs WHERE Username=? AND Password=?)", (chosen_user, chosen_pass,)) 
      valid=cursor.fetchone()
      if valid:
        messagebox.showinfo("Message", f"Entering 4quadGUI")
        dbHandler.save_table(conn, cursor)
        enter_4quadgui=True
        log_in.destroy()
      else:
        messagebox.showinfo("Message", f"Invalid username and/or incorrect password. Please try again or create new account.")
    
    #Creates the username Label and Entry for the user to input the username
    username=StringVar()
    user_name_label=Label(log_in, text="Enter username (Under 20 characters): ")
    user_name_label.grid(row=0, column=0)
    user_name=Entry(log_in, textvariable=username, validate="key", validatecommand=(user_verify, '%P'))
    user_name.grid(row=0, column=1)
    
    #Creates the username Label and Entry for the user to input the password
    password=StringVar()
    pass_word_label=Label(log_in, text="Enter password (Under 20 characters): ")
    pass_word_label.grid(row=0, column=2)
    pass_word=Entry(log_in, textvariable=password, validate="key", validatecommand=(password_verify, '%P')) 
    pass_word.grid(row=0, column=3)
    
    #Creates the button to initiate the check_log_in function
    log_in_butt=Button(log_in, text="Log in", command=check_log_in)
    log_in_butt.grid(row=1, column=0)
    
    #Creates the return button to allow the user to return to the initial GUI
    return_log=Button(log_in, text="Return", command=go_back_log)
    return_log.grid(row=1, column=2)
  
  #Creates the button to create the log in GUI
  pls_log = Button(sign_in, text="Log in to an existing account", command=log_in_func)
  pls_log.grid(row=0, column=0)

  #Creates the button to create the create_acc GUI
  pls_create = Button(sign_in, text="Create new account", command=create_account_func)
  pls_create.grid(row=0, column=1)
  
  #Creates the button to allow the user to exit the program
  quit_button=Button(sign_in, text="Exit", command=quit)
  quit_button.grid(row=0, column=2)
  
  #Creates the sign_in GUI
  sign_in.mainloop()

#Opens the initial GUI for the first time
sign_in_func()

