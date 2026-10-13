#Imports library to set up a reciever and communcation
from flask import Flask, jsonify, request
#Import the motor control library
from motor import MotorDriver
import time

#Creates a reciever
app = Flask(__name__)

#Forward function
def FWD():
    print("this is a motor driver test code")
    Motor = MotorDriver()
    
    print("forward 1 s")
    #one of the motors is flipped
    Motor.MotorRun(0, 'forward', 50)
    Motor.MotorRun(1, 'backward', 50)
    time.sleep(1)
    
    print("stop")
    Motor.MotorStop(0)
    Motor.MotorStop(1)


#Backward Function
def BACKWD():
    print("Moving backward")

#Left function
def LEFT():
    print("Turning left")

#Right function
def RIGHT():
    print("Turning right")

#PLay function
def PLAY():
    print("Playing")

#Stop function
def STOP():
    print("Stopping rover")

#Establishes receiving function
@app.route("/command", methods=["POST"])
def command():
    #retrieves message
    data = request.get_json(silent=True) or {}
    action = data.get("action")

    commands = {
        "forward": FWD,
        "backward": BACKWD,
        "left": LEFT,
        "right": RIGHT,
        "play": PLAY,
        "stop": STOP
    }

    #returns error if message is invalid command
    if action not in commands:
        return jsonify({"error": "Invalid command"}), 400

    #executes the command
    commands[action]()

    #returns success message
    return jsonify({
        "status": "success",
        "command": action
    })

#initializes the IP and Port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
