#import database management library
import sqlite3
from pathlib import Path
#import web application system
from flask import request, redirect, render_template

#Create a function to setup routes, obtains access to the important app varialbe
def setup_routes(app):
    #Setup web page route and alert user if there is a message
    @app.route("/")
    @app.route("/login.html")
    def login_page():
        message = request.args.get("message")
        return render_template("login.html", message=message)

    #Request DB to check login credentials
    @app.route("/login", methods=["POST"])
    def loginForm():
        username = request.form.get("username")
        password = request.form.get("password")

        #Connects to database
        conn = sqlite3.connect(Path(__file__).with_name("users.db"))
        cursor = conn.cursor()

        #Fetches database
        cursor.execute(
            "SELECT * FROM USERBASE WHERE Username = ? AND Password = ?",
            (username, password)
        )
        output = cursor.fetchone()
        conn.close()

        #Redirect to GUI page if credentials are validated
        if output:
            return redirect(
                "/index.html?message=Successfully%20logged%20in!"
            )

        #Return to login page if credentials are invalid
        return redirect(
            "/login.html?message=Incorrect%20username%20or%20password!"
        )
