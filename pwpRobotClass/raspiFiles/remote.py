#Imports library to set up a reciever and communcation
from flask import Flask, jsonify, request
#Import the motor control library
from motor import MotorDriver
#Imports for the video stream (camera, sockets, background thread)
import cv2
import socket
import struct
import threading
import time
import os

#IP of the computer running the GUI that receives the video
VIDEO_SERVER_IP = os.environ.get("VIDEO_SERVER_IP", "CHANGE_ME")
#Two cameras, each in its own pipe (own port, own socket, own thread)
#Must match VIDEO_PORT_1 / VIDEO_PORT_2 in config.py on the GUI computer
VIDEO_PORT_1 = 5002
VIDEO_PORT_2 = 5003
#Camera device numbers (/dev/videoN). Some USB cameras take two numbers each,
#so if camera 2 won't open try 2 instead of 1 (check with: ls /dev/video*)
CAMERA_INDEX_1 = 0
CAMERA_INDEX_2 = 1
JPEG_QUALITY = 80
RETRY_DELAY = 2 #seconds to wait before reconnecting

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

"""Video streaming
Each frame is JPEG-compressed by cv2.imencode, which returns a 1-D uint8 numpy array.
That array's bytes are sent with a 4-byte big-endian length header ("!I").
Receiver rebuilds the numpy array with: np.frombuffer(data, dtype=np.uint8)
then turns it back into an image with: cv2.imdecode(array, cv2.IMREAD_COLOR)"""

#Background thread for one camera: keeps (re)connecting to the GUI and streams frames until stopEvent is set
#Each camera runs this in its own thread with its own camera index and port
def sendFrames(name, cameraIndex, serverIP, port, stopEvent):
    #open the camera first so we never hold a connection without a camera
    camera = cv2.VideoCapture(cameraIndex)
    if not camera.isOpened():
        print(f"{name}: could not open camera {cameraIndex}, this stream is disabled")
        return

    try:
        #keeps reconnecting until told to stop, so the GUI can be started before or after the Pi
        while not stopEvent.is_set():
            try:
                videoSocket = socket.create_connection((serverIP, port), timeout=5)
            except OSError:
                print(f"{name}: no receiver at {serverIP}:{port}, retrying in {RETRY_DELAY}s")
                stopEvent.wait(RETRY_DELAY)
                continue

            print(f"{name}: streaming camera {cameraIndex} to {serverIP}:{port}")
            try:
                streamFrames(camera, videoSocket, stopEvent)
            except OSError:
                #covers BrokenPipeError, ConnectionResetError and send timeouts
                print(f"{name}: receiver disconnected")
            finally:
                videoSocket.close()
    finally:
        #releasing the camera
        camera.release()
        print(f"{name}: stopped")

#Sends frames over one connection until it breaks or we are told to stop
def streamFrames(camera, videoSocket, stopEvent):
    while not stopEvent.is_set():
        ret, frame = camera.read() #reading the frame
        if not ret:
            #camera hiccup, wait briefly instead of spinning the CPU
            time.sleep(0.01)
            continue

        #frame = cv2.resize(frame, (640, 480)) optional frame resize to fit GUI

        #buffer is a numpy array holding the compressed .jpg
        ok, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
        if not ok:
            continue
        data = buffer.tobytes()

        #message size so that the receiver knows how many bytes to read (header)
        msgSize = struct.pack("!I", len(data))
        videoSocket.sendall(msgSize + data)

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
    #starts each camera stream in its own background thread so they run alongside the Flask server
    #VIDEO_SERVER_IP must be the IP of the computer running the GUI (set it as an env var or edit the default)
    #stopVideo tells both video threads to finish; daemon=True so they can't keep the program alive
    stopVideo = threading.Event()
    videoThread1 = threading.Thread(target=sendFrames,
        args=("Video 1", CAMERA_INDEX_1, VIDEO_SERVER_IP, VIDEO_PORT_1, stopVideo), daemon=True)
    videoThread2 = threading.Thread(target=sendFrames,
        args=("Video 2", CAMERA_INDEX_2, VIDEO_SERVER_IP, VIDEO_PORT_2, stopVideo), daemon=True)
    videoThread1.start()
    videoThread2.start()
    try:
        #use_reloader=False so Flask doesn't spawn a second process that would also grab the cameras
        app.run(host="0.0.0.0", port=5001, threaded=True, use_reloader=False)
    finally:
        stopVideo.set()
        videoThread1.join(timeout=3)
        videoThread2.join(timeout=3)
        STOP()
