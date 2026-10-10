
import sqlite3
from flask import request, redirect


def setup_routes(app):

    @app.route("/create-account", methods=["POST"])
    def create_account():
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("pwpProjectLocal/users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM USERBASE WHERE Username = ?",
            (username,)
        )

        output = cursor.fetchone()

        if output:
            conn.close()
            return redirect(
                "/signup.html?message=Username%20already%20exists"
            )

        cursor.execute(
            "INSERT INTO USERBASE (Username, Password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect(
            "/login.html?message=Account%20creation%20successful!"
        )
