# Receives the two camera streams from the Pi (raspiFiles/remote.py) and shows them on the GUI page
# Plugs into main.py the same way as login/signup/rover: video_recieve.setup_routes(app)
#
# Each camera has its own pipe (its own TCP port, listener thread and frame buffer):
#    stream 1 -> config.VIDEO_PORT_1 -> /video_feed/1 (top-left box on index.html)
#    stream 2 -> config.VIDEO_PORT_2 -> /video_feed/2 (bottom-left box on index.html)
#
# Wire format sent by the Pi, per frame:
#    4-byte unsigned int header ("I"), followed by pickled numpy array data (pickle.dumps(buffer))
#
# The browser gets each stream as MJPEG, so index.html only needs <img src="/video_feed/1">
# Python code that wants a frame as a numpy image can call get_latest_frame(1) or get_latest_frame(2)

import socket
import struct
import threading
import pickle
import numpy as np
import cv2
# web application library
from flask import Response, abort
# imports the private settings
import config

HOST = "" # listening for a connection, not making one
HEADER = struct.Struct("I") # matches struct.pack("I", ...) in remote.py
MAX_FRAME_SIZE = 10 * 1024 * 1024 # ignore anything bigger than 10 MB
CONNECTION_TIMEOUT = 5 # seconds without data before the Pi is treated as disconnected

# One pipe: listens on its own port and keeps its own latest frame
class VideoStream:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        # latest JPEG bytes received; frameReady wakes up browsers waiting for a new frame
        self.latestJpeg = None
        self.frameReady = threading.Condition()
        self.started = False
        self.startLock = threading.Lock()

    # handles one connection from the Pi using File 1's robust buffering and unpickling logic
    def receiveFrames(self, sock):
        data = b""
        payload_size = HEADER.size

        try:
            while True:
                # 1. Read the header to get the exact size of the incoming frame payload
                while len(data) < payload_size:
                    packet = sock.recv(4 * 1024)
                    if not packet:
                        return
                    data += packet
                
                if len(data) < payload_size:
                    return

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = HEADER.unpack(packed_msg_size)[0]

                if msg_size == 0 or msg_size > MAX_FRAME_SIZE:
                    print(f"{self.name}: bad frame size {msg_size}, dropping connection")
                    return

                # 2. Read the actual frame data until we have the full message size
                while len(data) < msg_size:
                    packet = sock.recv(4 * 1024)
                    if not packet:
                        return
                    data += packet
                
                if len(data) < msg_size:
                    return

                frame_data = data[:msg_size]
                data = data[msg_size:]

                # 3. Unpickle and extract raw JPEG bytes so Flask/MJPEG can serve it
                frame_buffer = pickle.loads(frame_data)
                
                # frame_buffer is a numpy ndarray from cv2.imencode; convert to bytes for MJPEG
                jpeg_bytes = frame_buffer.tobytes() if hasattr(frame_buffer, 'tobytes') else bytes(frame_buffer)

                # 4. Save the frame and wake up any browser waiting on this stream
                with self.frameReady:
                    self.latestJpeg = jpeg_bytes
                    self.frameReady.notify_all()

        except Exception as e:
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
        lastSent = None
        while True:
            with self.frameReady:
                # wait for a frame we haven't sent yet
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

# the two separate pipes
streams = {
    1: VideoStream("Video 1", config.VIDEO_PORT_1),
    2: VideoStream("Video 2", config.VIDEO_PORT_2),
}

# returns the newest frame of a stream as a numpy image (height x width x 3, BGR), or None if none yet
def get_latest_frame(streamId):
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
