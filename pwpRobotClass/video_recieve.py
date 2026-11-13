# Receives the two camera streams from the Pi (raspiFiles/remote.py) and shows them on the GUI page
# Plugs into main.py the same way as login/signup/rover: video_recieve.setup_routes(app)
#
# Each camera has its own pipe (its own TCP port, listener thread and frame buffer):
#    stream 1 -> config.VIDEO_PORT_1 -> /video_feed/1 (top-left box on index.html)
#    stream 2 -> config.VIDEO_PORT_2 -> /video_feed/2 (bottom-left box on index.html)
#
# Wire format sent by the Pi, per frame:
#    4-byte unsigned int header ("!I"), followed by raw JPEG bytes from cv2.imencode
#
# The browser gets each stream as MJPEG, so index.html only needs <img src="/video_feed/1">
# Python code that wants a frame as a numpy image can call get_latest_frame(1) or get_latest_frame(2)

import socket
import struct
import threading
import numpy as np
import cv2
# web application library
from flask import Response, abort
# imports the private settings
import config

HOST = "" # listening for a connection, not making one
HEADER = struct.Struct("!I") # matches struct.pack("!I", ...) in videoSending.py
MAX_FRAME_SIZE = 10 * 1024 * 1024 # ignore anything bigger than 10 MB
CONNECTION_TIMEOUT = 5 # seconds without data before the Pi is treated as disconnected

# One pipe: listens on its own port and keeps its own latest frame
class VideoStream:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        # latest JPEG bytes received; frameReady wakes up browsers waiting for a new frame
        self.latestJpeg = None
        self.frameNumber = 0
        self.frameReady = threading.Condition()
        self.started = False
        self.startLock = threading.Lock()

    # reads exactly the requested number of bytes from the socket
    def receiveExact(self, sock, size):
        data = bytearray()
        while len(data) < size:
            packet = sock.recv(min(4096, size - len(data)))
            if not packet:
                return None
            data.extend(packet)
        return bytes(data)

    # handles one connection from the Pi and receives raw JPEG frames
    def receiveFrames(self, sock):
        try:
            while True:
                # 1. Read the header to get the exact size of the incoming frame payload
                packedMsgSize = self.receiveExact(sock, HEADER.size)
                if packedMsgSize is None:
                    return
                msgSize = HEADER.unpack(packedMsgSize)[0]

                if msgSize == 0 or msgSize > MAX_FRAME_SIZE:
                    print(f"{self.name}: bad frame size {msgSize}, dropping connection")
                    return

                # 2. Read the actual JPEG data until we have the full message size
                frameData = self.receiveExact(sock, msgSize)
                if frameData is None:
                    return

                # 3. Save the JPEG bytes and wake up any browser waiting on this stream
                with self.frameReady:
                    self.latestJpeg = frameData
                    self.frameNumber += 1
                    self.frameReady.notify_all()

        except (OSError, ValueError) as e:
            print(f"{self.name} stream error: {e}")

    # background thread: waits for the Pi to connect, receives frames, then waits again
    def listener(self):
        listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listeningSocket.bind((HOST, self.port))
        listeningSocket.listen(1)
        print(f"{self.name}: waiting for the Pi on port {self.port}")

        while True:
            sock, addr = listeningSocket.accept()
            print(f"{self.name}: Pi connected from {addr[0]}")
            # timeout so a Pi that drops off Wi-Fi doesn't leave us waiting forever
            sock.settimeout(CONNECTION_TIMEOUT)
            try:
                self.receiveFrames(sock)
            except OSError: # covers timeouts and connection resets
                pass
            finally:
                sock.close()
            print(f"{self.name}: Pi disconnected")

    # starts the listener once; called on the first request for this stream
    def start(self):
        with self.startLock:
            if not self.started:
                threading.Thread(target=self.listener, daemon=True).start()
                self.started = True

    # yields each new frame in the multipart format browsers understand as live video
    def mjpegStream(self):
        lastSent = 0
        while True:
            with self.frameReady:
                # wait for a frame we haven't sent yet
                self.frameReady.wait_for(
                    lambda: self.frameNumber != lastSent, timeout=5)
                jpeg = self.latestJpeg
                currentFrame = self.frameNumber
            if jpeg is None or currentFrame == lastSent:
                continue
            lastSent = currentFrame
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n"
                   b"Content-Length: " + str(len(jpeg)).encode() + b"\r\n\r\n" +
                   jpeg + b"\r\n")

# the two separate pipes
streams = {
    1: VideoStream("Video 1", config.VIDEO_PORT_1),
    2: VideoStream("Video 2", config.VIDEO_PORT_2),
}

# returns the newest frame of a stream as a numpy image (height x width x 3, BGR), or None if none yet
def get_latest_frame(streamId):
    if streamId not in streams:
        return None
    with streams[streamId].frameReady:
        jpeg = streams[streamId].latestJpeg
    if jpeg is None:
        return None
    return cv2.imdecode(np.frombuffer(jpeg, dtype=np.uint8), cv2.IMREAD_COLOR)

# Create a function to setup routes, obtains access to the important app variable
def setup_routes(app):
    # live video for the <img> tags on index.html
    @app.route("/video_feed/<int:streamId>")
    def video_feed(streamId):
        if streamId not in streams:
            abort(404)
        stream = streams[streamId]
        stream.start()
        return Response(stream.mjpegStream(), mimetype="multipart/x-mixed-replace; boundary=frame")