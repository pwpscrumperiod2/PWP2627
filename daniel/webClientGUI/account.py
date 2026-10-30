import sqlite3
import tkinter as tk
from tkinter import messagebox

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
radio_var = tk.IntVar()
radio_button1=tk.Radiobutton(displayMain,text="Login",variable=radio_var,value=1)
radio_button1.pack()
radio_button2=tk.Radiobutton(displayMain,text="Create Account",variable=radio_var,value=2)
radio_button2.pack()


#username and password variables
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
entry2 = tk.Entry(displayMain, textvariable=e2, show="*")
entry2.pack(padx=3, pady=5)




#Database Connection
def retrieve_input():
    global loggedIn
    global displayMain
    if e1.get() == '' or e2.get() == '':
        messagebox.showinfo("Notification", "Please type a username and password")
        return


    if len(e1.get()) > 16 or len(e2.get()) > 16:
        messagebox.showinfo("Notification", "Please keep username and password under 16 characters")
        return


    #create and connect to sql
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()


    if radio_var.get() == 0:
        #nothing selected
        messagebox.showinfo("Problem", "Please choose an action and try again")


    if radio_var.get() == 1:
        #login to account
        if e1.get() in [username[0] for username in cursor.execute("SELECT Username from USERBASE")]:
            #username is valid
            query = "SELECT Password from USERBASE WHERE Username = ?"
            params = [e1.get()]
            if e2.get() in [password[0] for password in cursor.execute(query, params)]:
                messagebox.showinfo("Notification", "Successfully Logged In")
                # ends this window
                displayMain.destroy()
                loggedIn = True
                return
            else:
                messagebox.showinfo("Notification", "Wrong Password")
        else:
            messagebox.showinfo("Notification", "Invalid username")


    if radio_var.get() == 2:
        cursor.execute("SELECT Username from USERBASE")
        if e1.get() in [username[0] for username in cursor.execute("SELECT Username from USERBASE")]:
            #username already in use
            messagebox.showinfo("Notification", "Username already used, use a different one")
        else:
            #username unused
            cursor.execute("SELECT * FROM USERBASE")
            query = "INSERT INTO USERBASE (Username, Password) VALUES (?,?)"
            params = (e1.get(), e2.get())
            cursor.execute(query, params)
            messagebox.showinfo("Notification", "Successfully created account")
        #create account


    #exit out of sql
    conn.commit()
    conn.close()
    return
#Submit Button
average_button = tk.Button(displayMain, text="Submit", command=retrieve_input)
average_button.pack(pady=10)


#Loop
displayMain.mainloop()
