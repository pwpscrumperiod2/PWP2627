#imports web application library
from flask import Flask, request, render_template
#imports the secondary files
import initialize_db
import login
import signup
import rover

#creates flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = "borat"

"""SETS UP WEB PAGES"""
#Directs login URL to login page
@app.route("/")
@app.route("/login.html")
def login_page():
    message = request.args.get("message")
    return render_template("login.html", message=message)


#Directs signup URL to signup page
@app.route("/signup.html")
def signup_page():
    message = request.args.get("message")
    return render_template("signup.html", message=message)


#Directs homepage to GUI page
@app.route("/index.html")
def home():
    message = request.args.get("message")
    return render_template("index.html", message=message)


# Register routes from other files
login.setup_routes(app)
signup.setup_routes(app)
rover.setup_routes(app)

#Initializes the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
