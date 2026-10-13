#Imports library to set up a reciever and communcation
from flask import Flask, jsonify, request
#Import the motor control library
from motor import MotorDriver
import time

#Creates a reciever
app = Flask(__name__)
Motor = MotorDriver()

#Forward function
def FWD():
    #fetches the motor object
    global Motor
    
    #one of the motors is flipped
    Motor.MotorRun(0, 'forward', 50)
    Motor.MotorRun(1, 'backward', 50)
    #one second of movement before stopping
    time.sleep(1)

    #stop the motors
    Motor.MotorStop(0)
    Motor.MotorStop(0)


#Backward Function
def BACKWD():
    #fetches the motor object
    global Motor
    
    #one of the motors is flipped, they are going backward
    Motor.MotorRun(0, 'backward', 50)
    Motor.MotorRun(1, 'forward', 50)
    #one second of movement before stopping
    time.sleep(1)

    #stop the motors
    Motor.MotorStop(0)
    Motor.MotorStop(0)

#Left function
def LEFT():
    #fetches the motor object
    global Motor
    
    #one of the motors is flipped, they are turning left
    Motor.MotorRun(0, 'backward', 50)
    Motor.MotorRun(1, 'backward', 50)
    #0.3 second of movement before stopping
    time.sleep(0.3)

    #stop the motors
    Motor.MotorStop(0)
    Motor.MotorStop(0)

#Right function
def RIGHT():
    #fetches the motor object
    global Motor
    
    #one of the motors is flipped, they are turning right
    Motor.MotorRun(0, 'forward', 50)
    Motor.MotorRun(1, 'forward', 50)
    #0.3 second of movement before stopping
    time.sleep(0.3)

    #stop the motors
    Motor.MotorStop(0)
    Motor.MotorStop(0)
#PLay function
def PLAY():
    print("Playing")

#Stop function
def STOP():
    #fetches the motor object
    global Motor
    #stop the motors
    Motor.MotorStop(0)
    Motor.MotorStop(1)
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
