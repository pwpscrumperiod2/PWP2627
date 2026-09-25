from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    text = "Hello, World!"

    if request.method == "POST":
        button = request.form.get("button")

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

    return render_template("index.html", text=text)


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

if __name__ == "__main__":
    app.run(debug=False)