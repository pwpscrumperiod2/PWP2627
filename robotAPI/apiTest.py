#import libraries for flask and to create the web app, and get info from forms
from flask import Flask, render_template, request

#Create the flask app
app = Flask(__name__)

#Define home page route to accept get and post requests
@app.route("/", methods=["GET", "POST"])
def home():
    #Default message
    text = "Hello, World!"

    #check if the form has been submitted
    if request.method == "POST":
        #gets value of the button clicked
        button = request.form.get("button")

        #determines function and output based on button value
        if button == "forward":
            FWD()
            text = "Forward Selected"
        elif button == "backward":
            BACKWD()
            text = "Backward Selected"
        elif button == "right":
            RIGHT()
            text = "Right Selected"
        elif button == "left":
            LEFT()
            text = "Left Selected"
        elif button == "stop":
            STOP()
            text = "Stopped"
    #load the html template and pass the text value on
    return render_template("index.html", text=text)

#Functions for the API; currently placeholders that just output terminal
def FWD():
    print("Forward")

def BACKWD():
    print("Backward")

def LEFT():
    print("Left")

def RIGHT():
    print("Right")

def STOP():
    print("Stop")

#start the application when running this file
if __name__ == "__main__":
    app.run(debug=False)