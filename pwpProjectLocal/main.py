from flask import Flask, request, render_template
import initialize_db
import login
import signup
import rover

app = Flask(__name__)
app.config["SECRET_KEY"] = "borat"


# Login page
@app.route("/")
@app.route("/login.html")
def login_page():
    message = request.args.get("message")
    return render_template("login.html", message=message)


# Signup page
@app.route("/signup.html")
def signup_page():
    message = request.args.get("message")
    return render_template("signup.html", message=message)


# Homepage
@app.route("/index.html")
def home():
    message = request.args.get("message")
    return render_template("index.html", message=message)


# Register routes from other files
login.setup_routes(app)
signup.setup_routes(app)
rover.setup_routes(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
