#import libraries for api functionality
import sqlite3
import json
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "borat"


#set login as default page
@app.route("/")
@app.route("/login.html")
def login():
    return render_template("login.html")

#loads signup page
@app.route("/index.html")
def home():
    return render_template("index.html")


#loads signup page
@app.route("/signup.html")
def signup():
    return render_template("signup.html")

#signals that the login button is clicked and starts communication with database
@app.route("/login", methods=["POST"])
def loginForm():
    print("Logged In")
    username = request.form.get("username")
    password = request.form.get("password")
    conn = sqlite3.connect("pwpProject_RobotAPI/users.db")
    cursor = conn.cursor()

    #Gets usernames and passwords
    cursor.execute(
        "SELECT * FROM USERBASE WHERE Username = ? AND Password = ?",(username, password),
    )
    output = cursor.fetchone()
    conn.close()
    #Checks if user exists or not
    if output:
        return redirect("index.html")
    else:
        return render_template("login.html", error="Incorrect username or password!")


@app.route("/create-account", methods=["POST"])
def create_account():
    username = request.form.get("username")
    password = request.form.get("password")
    conn = sqlite3.connect("pwpProject_RobotAPI/users.db")
    cursor = conn.cursor()

    #Gets usernames and passwords
    cursor.execute(
        "SELECT * FROM USERBASE WHERE Username = ?",(username,),
    )
    output = cursor.fetchone()

    #Username already taken
    if output:
        conn.close()
        return render_template("signup.html", error="Username already exists")
    #Successfull account creation
    cursor.execute(
        "INSERT INTO USERBASE (Username, Password) VALUES (?, ?)",
        (username, password),
    )
    conn.commit()
    conn.close()
    return render_template("/login.html", error="Account creation successful!")




#runs the file
if __name__ == "__main__":
    app.run(debug=True)


