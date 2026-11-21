#Imports library to set up a reciever and communcation
from flask import Flask, jsonify, request
#Import the motor control library
from motor import MotorDriver

#Creates a reciever
app = Flask(__name__)
Motor = MotorDriver()


"""Motor 0 is the motor on the right side of the rover; it is stronger than the motor on th left side of the rover"""
#Forward function
def FWD():
    #fetches the motor object
    global Motor
    
    #one of the motors is flipped, different speeds to calibrate
    Motor.MotorRun(0, 'forward', 56)
    Motor.MotorRun(1, 'backward', 64)

#Backward Function
def BACKWD():
    #fetches the motor object
    global Motor
    
    #one of the motors is flipped, different speeds to calibrate
    Motor.MotorRun(0, 'backward', 62)
    Motor.MotorRun(1, 'forward', 66)

#Left turning function
def LEFT():
    #fetches the motor object
    global Motor
    
    #one of the motors is flipped, they are turning left
    Motor.MotorRun(0, 'forward', 50)
    Motor.MotorRun(1, 'forward', 50)

#Right turning function
def RIGHT():
    #fetches the motor object
    global Motor
    
    #one of the motors is flipped, they are turning right
    Motor.MotorRun(0, 'backward', 50)
    Motor.MotorRun(1, 'backward', 50)

#PLay function
def PLAY():
    #4 Instances of forward to move the designated distance
    for i in range(4):
        FWD()
    #6 instances of right turning to turn 90 degrees
    for i in range(6):
        RIGHT()
    #5 instances of backwards movement to cross the path
    for i in range(5):
        BACKWD()
    #3 Instances of forward to move back to the center
    for i in range(3):
        FWD()
    #4 instances of left turning to return to starting alignment
    for i in range(4):
        LEFT()
    #3 instances of backwards movement to reverse into starting position
    for i in range(3):
        BACKWD()

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

    #matches each command name to the function that runs it
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

    #executes the command by calling the matching function
    commands[action]()

    #returns success message
    return jsonify({
        "status": "success",
        "command": action
    })

#initializes the IP and Port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
