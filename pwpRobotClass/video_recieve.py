#Receives the two camera streams from the Pi (raspiFiles/remote.py) and shows them on the GUI page
#Plugs into main.py the same way as login/signup/rover: video_recieve.setup_routes(app)
#
#Each camera has its own pipe (its own TCP port, listener thread and frame buffer):
#   stream 1 -> config.VIDEO_PORT_1 -> /video_feed/1 (top-left box on index.html)
#   stream 2 -> config.VIDEO_PORT_2 -> /video_feed/2 (bottom-left box on index.html)
#
#Wire format sent by the Pi, per frame:
#   4-byte big-endian length header ("!I"), then the bytes of a JPEG numpy array (from cv2.imencode)
#
#The browser gets each stream as MJPEG, so index.html only needs <img src="/video_feed/1">
#Python code that wants a frame as a numpy image can call get_latest_frame(1) or get_latest_frame(2)

#imports sockets and threading for background running
import socket
import struct
import threading
#web application library
from flask import Response, abort
#imports the private settings
import config

HOST = "" #listening for a connection, not making one
HEADER = struct.Struct("!I") #must match struct.pack("!I", ...) in remote.py
MAX_FRAME_SIZE = 1000 * 1024 * 1024 #ignore anything bigger than 10 MB, it isn't a real frame
CONNECTION_TIMEOUT = 5 #seconds without data before the Pi is treated as disconnected

#reads exactly `size` bytes, or returns None if the Pi disconnected
def recvExactly(sock, size):
    data = bytearray()
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return None
        data.extend(chunk)
    return bytes(data)

#One pipe: listens on its own port and keeps its own latest frame
class VideoStream:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        #latest JPEG received; frameReady wakes up browsers waiting for a new frame
        self.latestJpeg = None
        self.frameReady = threading.Condition()
        self.started = False
        self.startLock = threading.Lock()

    #handles one connection from the Pi until it disconnects
    def receiveFrames(self, sock):
        while True:
            header = recvExactly(sock, HEADER.size)
            if header is None:
                return
            (frameSize,) = HEADER.unpack(header)

            if frameSize == 0 or frameSize > MAX_FRAME_SIZE:
                print(f"{self.name}: bad frame size {frameSize}, dropping connection")
                return
            print('something recieved')
            jpeg = recvExactly(sock, frameSize)
            if jpeg is None:
                return

            #saves the frame and wakes up any browser waiting on this stream
            with self.frameReady:
                self.latestJpeg = jpeg
                self.frameReady.notify_all()

    #background thread: waits for the Pi to connect, receives frames, then waits again
    def listener(self):
        listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listeningSocket.bind((HOST, self.port))
        listeningSocket.listen(1)
        print(f"{self.name}: waiting for the Pi on port {self.port}")

        while True:
            sock, addr = listeningSocket.accept()
            print(f"{self.name}: Pi connected from {addr[0]}")
            #timeout so a Pi that drops off Wi-Fi doesn't leave us waiting forever
            sock.settimeout(CONNECTION_TIMEOUT)
            try:
                self.receiveFrames(sock)
            except OSError: #covers timeouts and connection resets
                pass
            finally:
                sock.close()
            print(f"{self.name}: Pi disconnected")

    #starts the listener once; called on the first request for this stream so that only the process
    #actually serving pages binds the port (Flask's debug reloader runs a second watcher process)
    def start(self):
        with self.startLock:
            if not self.started:
                threading.Thread(target=self.listener, daemon=True).start()
                self.started = True

    #yields each new frame in the multipart format browsers understand as live video
    def mjpegStream(self):
        lastSent = None
        while True:
            with self.frameReady:
                #wait for a frame we haven't sent yet (timeout so we re-check now and then)
                self.frameReady.wait_for(
                    lambda: self.latestJpeg is not None and self.latestJpeg is not lastSent, timeout=5)
                jpeg = self.latestJpeg
            if jpeg is None or jpeg is lastSent:
                continue
            lastSent = jpeg
            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n"
                   b"Content-Length: " + str(len(jpeg)).encode() + b"\r\n\r\n" +
                   jpeg + b"\r\n")

#the two separate pipes
streams = {
    1: VideoStream("Video 1", config.VIDEO_PORT_1),
    2: VideoStream("Video 2", config.VIDEO_PORT_2),
}

#returns the newest frame of a stream as a numpy image (height x width x 3, BGR), or None if none yet
def get_latest_frame(streamId):
    import numpy as np
    import cv2
    jpeg = streams[streamId].latestJpeg
    if jpeg is None:
        return None
    return cv2.imdecode(np.frombuffer(jpeg, dtype=np.uint8), cv2.IMREAD_COLOR)

#Create a function to setup routes, obtains access to the important app varialbe
def setup_routes(app):
    #live video for the <img> tags on index.html
    @app.route("/video_feed/<int:streamId>")
    def video_feed(streamId):
        if streamId not in streams:
            abort(404)
        stream = streams[streamId]
        stream.start()
        return Response(stream.mjpegStream(), mimetype="multipart/x-mixed-replace; boundary=frame")
