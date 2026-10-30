#import database management library
import sqlite3
from pathlib import Path
#import web application system
from flask import request, redirect, render_template

#Create a function to setup routes, obtains access to the important app varialbe
def setup_routes(app):
    #Directs signup URL to signup page and display a message if one existsa
    @app.route("/signup.html")
    def signup_page():
        message = request.args.get("message")
        return render_template("signup.html", message=message)

    #Request DB to create account
    @app.route("/create-account", methods=["POST"])
    def create_account():
        username = request.form.get("username")
        password = request.form.get("password")

        #Connects to database
        conn = sqlite3.connect(Path(__file__).with_name("users.db"))
        cursor = conn.cursor()

        #Fetches Database
        cursor.execute(
            "SELECT * FROM USERBASE WHERE Username = ?",
            (username,)
        )

        output = cursor.fetchone()
        #Return error if there is conflict
        if output:
            conn.close()
            return redirect(
                "/signup.html?message=Username%20already%20exists"
            )

        #Save to database and close if successful
        cursor.execute(
            "INSERT INTO USERBASE (Username, Password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        conn.close()

        #Sends to login page after creating account
        return redirect(
            "/login.html?message=Account%20creation%20successful!"
        )
