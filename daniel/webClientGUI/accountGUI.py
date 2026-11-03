#import GUI library and its popup windows
import tkinter as tk
from tkinter import messagebox
import accountdb

#becomes True after a successful login, main.py checks this to open the home screen
loggedIn = False

#Set Up Tkinter Window
displayMain = tk.Tk()
displayMain.geometry("1000x1000")
displayMain.title("GigaBite Login Page")
displayMain.resizable(True, True)


#Title
label1 = tk.Label(displayMain, text="GigaBite Login Page")
label1.pack(fill="x", padx=3, pady=5)
label1.config(font=("Futura", 44))


#Choose an action
label1 = tk.Label(displayMain, text="Choose an action")
label1.pack(fill="x", padx=3, pady=5)
label1.config(font=("Futura", 34))


#Choose Login or Create Account
#radio_var is 0 when nothing is picked, 1 for Login, 2 for Create Account
radio_var = tk.IntVar()
radio_button1=tk.Radiobutton(displayMain,text="Login",variable=radio_var,value=1)
radio_button1.pack()
radio_button2=tk.Radiobutton(displayMain,text="Create Account",variable=radio_var,value=2)
radio_button2.pack()


#username and password variables
#e1 holds the username, e2 holds the password
e1 = tk.StringVar()
e2 = tk.StringVar()


#Username
userLabel = tk.Label(displayMain, text="Username")
userLabel.pack(fill="x", padx=3, pady=5)
userLabel.config(font=("Futura", 30))
entry1 = tk.Entry(displayMain, textvariable=e1)
entry1.pack(padx=3, pady=5)


#Password
passLabel = tk.Label(displayMain, text="Password")
passLabel.pack(fill="x", padx=3, pady=5)
passLabel.config(font=("Futura", 30))
#show="*" hides the password as it is typed
entry2 = tk.Entry(displayMain, textvariable=e2, show="*")
entry2.pack(padx=3, pady=5)


#Database Connection
#runs when the Submit button is clicked, logs in or creates an account
def retrieve_input():
    global loggedIn
    global displayMain
    #make sure both boxes were filled in
    if e1.get() == '' or e2.get() == '':
        messagebox.showinfo("Notification", "Please type a username and password")
        return

    #the database only allows 16 characters for each
    if len(e1.get()) > 16 or len(e2.get()) > 16:
        messagebox.showinfo("Notification", "Please keep username and password under 16 characters")
        return
    
    if radio_var.get() == 0:
        #nothing selected
        messagebox.showinfo("Problem", "Please choose an action and try again")

    #check the database for the account
    if accountdb.check_account(radio_var.get(), e1, e2):
        loggedIn = True
        displayMain.destroy()
    return

#Submit Button
average_button = tk.Button(displayMain, text="Submit", command=retrieve_input)
average_button.pack(pady=10)


#Loop
#keeps the window open until it is closed or the user logs in
displayMain.mainloop()
