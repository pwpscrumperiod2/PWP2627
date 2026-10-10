
import sqlite3
from flask import request, redirect


def setup_routes(app):

    @app.route("/login", methods=["POST"])
    def loginForm():
        print("Logged In")

        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("pwpProjectLocal/users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM USERBASE WHERE Username = ? AND Password = ?",
            (username, password)
        )

        output = cursor.fetchone()
        conn.close()

        if output:
            return redirect(
                "/index.html?message=Successfully%20logged%20in!"
            )

        return redirect(
            "/login.html?message=Incorrect%20username%20or%20password!"
        )
