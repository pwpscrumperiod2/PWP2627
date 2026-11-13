#Imports library to set up a reciever and communcation
from flask import Flask, jsonify, request
#Import the motor control library
from motor import MotorDriver
#Imports for the video stream
from videoSending import startVideoStreams

#IP of the computer running the GUI that receives the video
VIDEO_SERVER_IP = "192.168.240.6"
#One camera sends the same frame to two separate connections
#Must match VIDEO_PORT_1 / VIDEO_PORT_2 in config.py on the GUI computer
VIDEO_PORT_1 = 5002
VIDEO_PORT_2 = 5003
#Camera device number (/dev/videoN)
CAMERA_INDEX = 0

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
    #3 Instances of forward to move the designated distance
    pass

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
    #starts one camera and sends each JPEG frame over both connections
    #VIDEO_SERVER_IP must be the IP of the computer running the GUI
    stopVideo, videoThreads = startVideoStreams(
        VIDEO_SERVER_IP,
        CAMERA_INDEX,
        (VIDEO_PORT_1, VIDEO_PORT_2)
    )
    try:
        #use_reloader=False so Flask doesn't spawn a second process that also grabs the camera
        app.run(host="0.0.0.0", port=5001, threaded=True, use_reloader=False)
    finally:
        stopVideo.set()
        for videoThread in videoThreads:
            videoThread.join(timeout=3)
            
        STOP()