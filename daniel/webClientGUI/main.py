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


# Register routes from other files
login.setup_routes(app)
signup.setup_routes(app)
rover.setup_routes(app)

#Initializes the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
