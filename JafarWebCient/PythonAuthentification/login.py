from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import main

# create the database
con = sqlite3.connect("User_Database.db")
cur = con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
UserID INTEGER PRIMARY KEY AUTOINCREMENT, 
Username TEXT UNIQUE NOT NULL,
Password TEXT NOT NULL )
""")
con.commit()

# create the original window
root = Tk()
root.geometry("1920x1080")
root.resizable(False, False)
root.title("Login Page")


# functions
def CreateAcc(a, b, c):

    if a == "":
        messagebox.showerror("Error", "Please enter a valid username")
        return

    elif "!" in a or "@" in a or "#" in a or "$" in a or "%" in a or "^" in a or "&" in a or "*" in a or "(" in a or ")" in a:
        messagebox.showerror("Error", "Please enter a valid username without special characters")
        return

    elif b != c:
        messagebox.showerror("Error", "Passwords do not match")
        return
    else:
        try:
            cur.execute("""
            INSERT INTO users (Username, Password)
            VALUES (?, ?)
            """,
            (a, b)
            )
            con.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
            return

        messagebox.showinfo("Success!", "Successfully logged in :)")
        Loginpage()

def Auth(a, b):
    if a == "" or b == "":
        messagebox.showerror("Error", "Please fill in all fields")
        return

    elif "!" in a or "@" in a or "#" in a or "$" in a or "%" in a or "^" in a or "&" in a or "*" in a or "(" in a or ")" in a:
        messagebox.showerror("Error", "Please enter a valid username without special characters")
        return

    else:
        cur.execute("""
        SELECT Password FROM users WHERE Username = ?
        """,
        (a,)
        )
        row = cur.fetchone()
        if row == None:
            messagebox.showerror("Error", "Incorrect Username or Password. Create New Account?")
            return

        if row[0] != b:
            messagebox.showerror("Error", "Incorrect Username or Password")
            return

        else:
            messagebox.showinfo("Success!", "Successfully logged in :)")
            for widget in root.winfo_children():
                widget.destroy()
            main.RunMainGUI(root)
            return

def Loginpage():
    for widget in root.winfo_children():
        widget.destroy()

    # Login button
    Login = Button(root, text="Login", command=Log, bg = "grey", width = 50, height = 10, font = ("Arial", 36, "bold"))
    Login.pack(expand=TRUE)

    # Signup button
    Signup = Button(root, text="Sign up", command=Sign, bg = "grey", width = 50, height = 5, font = ("Arial", 36, "bold"))
    Signup.pack(expand=TRUE)

def Sign():
    anewname = StringVar()
    anewpassword = StringVar()
    confirmedpass = StringVar()

    for widget in root.winfo_children():
        widget.destroy()

    Signupframe = Frame(root, width = 400, height = 600, borderwidth = 2, bg="white", relief = "sunken")
    Signupframe.pack(expand=TRUE)
    Signupframe.columnconfigure(0, minsize=100)
    Signupframe.rowconfigure(0, minsize=100)

    Titlelabel = Label(Signupframe, text = "Sign Up", bg = "white", font = ("Arial", 36, "bold", "underline"))
    Titlelabel.grid(row = 0, column = 0, columnspan = 2)

    LabelforNewuser = Label(Signupframe, text="Create New User: ", font = ("Arial", 18, "bold"))
    LabelforNewuser.grid(row = 1, column = 0, sticky = W)
    Newuser = Entry(Signupframe, textvariable=anewname)
    Newuser.grid(row = 1, column = 1, sticky = E)

    LabelforNewpassword = Label(Signupframe, text="Create New Password: ", font=("Arial", 18, "bold"))
    LabelforNewpassword.grid(row=2, column=0, sticky=W)
    Newpassword = Entry(Signupframe, textvariable=anewpassword)
    Newpassword.grid(row=2, column=1, sticky=E)

    LabelforConfirmpassword = Label(Signupframe, text="Confirm New Password: ", font=("Arial", 18, "bold"))
    LabelforConfirmpassword.grid(row=3, column=0, sticky=W)
    Confirmpassword = Entry(Signupframe, textvariable=confirmedpass)
    Confirmpassword.grid(row=3, column=1, sticky=E)

    Createnewaccount = Button(Signupframe, text="Create New Account", command=lambda: CreateAcc(anewname.get(), anewpassword.get(), confirmedpass.get()))
    Createnewaccount.grid(row=4, column=1, columnspan = 2)

    Exitbutton = Button(Signupframe, text="Exit", command=Loginpage)
    Exitbutton.grid(row=4, column=0, columnspan = 1)

def Log():
    for widget in root.winfo_children():
        widget.destroy()

    userlogin = StringVar()
    userpassword = StringVar()

    Loginframe = Frame(root, width=400, height=600, borderwidth=2, bg="white", relief="sunken")
    Loginframe.pack(expand=TRUE)
    Loginframe.columnconfigure(0, minsize=100)
    Loginframe.rowconfigure(0, minsize=100)

    Titlelabel = Label(Loginframe, text="Log In", bg="white", font=("Arial", 36, "bold", "underline"))
    Titlelabel.grid(row=0, column=0, columnspan=2)

    Labelforuser = Label(Loginframe, text="Username: ", font=("Arial", 18, "bold"))
    Labelforuser.grid(row=1, column=0, sticky=W)
    user = Entry(Loginframe, textvariable=userlogin)
    user.grid(row=1, column=1, sticky=E)

    Labelforpassword = Label(Loginframe, text="Password: ", font=("Arial", 18, "bold"))
    Labelforpassword.grid(row=2, column=0, sticky=W)
    password = Entry(Loginframe, textvariable=userpassword)
    password.grid(row=2, column=1, sticky=E)

    Logintomenu = Button(Loginframe, text="Login to GUI", command=lambda: Auth(userlogin.get(), userpassword.get()))
    Logintomenu.grid(row=4, column=1, columnspan=2)

    Exitbutton = Button(Loginframe, text="Exit", command=Loginpage)
    Exitbutton.grid(row=4, column=0, columnspan=1)

Loginpage()
root.mainloop()


