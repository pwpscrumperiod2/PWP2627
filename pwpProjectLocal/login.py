#import database management library
import sqlite3
#import web application system
from flask import request, redirect

#Create a function to setup routes, obtains access to the important app varialbe
def setup_routes(app):

    #Request DB to check login credentials
    @app.route("/login", methods=["POST"])
    def loginForm():
        username = request.form.get("username")
        password = request.form.get("password")

        #Connects to database
        conn = sqlite3.connect("pwpProjectLocal/users.db")
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
