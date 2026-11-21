from tkinter import *
from AccountCreation import *
from Auth import *
import sqlite3

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
con.close()

def RunLoginGUI(root):
    root.geometry("1920x1080")
    root.resizable(False, False)
    root.title("Login Page")

    for widget in root.winfo_children():
        widget.destroy()


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

        Createnewaccount = Button(Signupframe, text="Create New Account", command=lambda: CreateAcc(anewname.get(), anewpassword.get(), confirmedpass.get(),Loginpage))
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

        Logintomenu = Button(Loginframe, text="Login to GUI", command=lambda: Auth(userlogin.get(), userpassword.get(),root))
        Logintomenu.grid(row=4, column=1, columnspan=2)

        Exitbutton = Button(Loginframe, text="Exit", command=Loginpage)
        Exitbutton.grid(row=4, column=0, columnspan=1)
    Loginpage()


