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

#runs the file
if __name__ == "__main__":
    app.run(debug=True)


