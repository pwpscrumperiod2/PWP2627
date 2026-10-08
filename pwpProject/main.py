#import libraries for api functionality
import sqlite3
from flask import Flask, jsonify, redirect, render_template, request

#creates flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "borat"


#set login as default page
@app.route("/")
@app.route("/login.html")
def login():
    message = request.args.get("message")
    return render_template("login.html", message=message)

#loads signup page
@app.route("/signup.html")
def signup():
    message = request.args.get("message")
    return render_template("signup.html", message=message)

#loads signup page
@app.route("/index.html")
def home():
    message = request.args.get("message")
    return render_template("index.html", message=message)


#signals that the login button is clicked and starts communication with database
@app.route("/login", methods=["POST"])
def loginForm():
    print("Logged In")
    username = request.form.get("username")
    password = request.form.get("password")
    conn = sqlite3.connect("pwpProject_RobotAPI/users.db")
    cursor = conn.cursor()

    #Gets usernames and passwords
    cursor.execute("SELECT * FROM USERBASE WHERE Username = ? AND Password = ?",(username, password),)
    output = cursor.fetchone()
    conn.close()
    #Checks if user exists or not
    if output:
        return redirect("/index.html?message=Successfully%20logged%20in!")
    else:
        return redirect("/login.html?message=Incorrect%20username%20or%20password!")

#signals that the sign up button is clicked and starts communication with database
@app.route("/create-account", methods=["POST"])
def create_account():
    username = request.form.get("username")
    password = request.form.get("password")
    conn = sqlite3.connect("pwpProject_RobotAPI/users.db")
    cursor = conn.cursor()

    #Gets usernames and passwords
    cursor.execute("SELECT * FROM USERBASE WHERE Username = ?",(username,),)
    output = cursor.fetchone()

    #Username already taken
    if output:
        conn.close()
        return redirect("/signup.html?message=Username%20already%20exists")
    #Successfull account creation
    cursor.execute(
        "INSERT INTO USERBASE (Username, Password) VALUES (?, ?)",
        (username, password),
    )
    conn.commit()
    conn.close()
    return redirect("/login.html?message=Account%20creation%20successful!")

# Handle the "up" action
@app.route("/up", methods=["POST"])
def up():
    return jsonify({
        "action": "up",
        "status_code": 200
    })


# Handle the "down" action
@app.route("/down", methods=["POST"])
def down():
    return jsonify({
        "action": "down",
        "status_code": 200
    })


# Handle the "right" action
@app.route("/right", methods=["POST"])
def right():
    return jsonify({
        "action": "right",
        "status_code": 200
    })


# Handle the "left" action
@app.route("/left", methods=["POST"])
def left():
    return jsonify({
        "action": "left",
        "status_code": 200
    })


# Handle the "play" action
@app.route("/play", methods=["POST"])
def play():
    return jsonify({
        "action": "play",
        "status_code": 200
    })


# Handle the "pause" action
@app.route("/stop", methods=["POST"])
def stop():
    return jsonify({
        "action": "stop",
        "status_code": 200
    })


#runs the file
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
