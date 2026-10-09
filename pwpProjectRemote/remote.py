from flask import Flask, jsonify, request

app = Flask(__name__)

def FWD():
    print("Moving forward")

def BACKWD():
    print("Moving backward")

def LEFT():
    print("Turning left")

def RIGHT():
    print("Turning right")

def STOP():
    print("Stopping rover")


@app.route("/command", methods=["POST"])
def command():
    data = request.get_json(silent=True) or {}
    action = data.get("action")

    commands = {
        "forward": FWD,
        "backward": BACKWD,
        "left": LEFT,
        "right": RIGHT,
        "stop": STOP
    }

    if action not in commands:
        return jsonify({"error": "Invalid command"}), 400

    commands[action]()

    return jsonify({
        "status": "success",
        "command": action
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
