#https://medium.com/@staytechrich/socket-002-sending-and-receiving-video-over-sockets-cf701e4ef814

import socket
import cv2
import struct
import time
import threading

JPEG_QUALITY = 80
RETRY_DELAY = 2 #seconds to wait before reconnecting

#Sends frames over one connection until it breaks or we are told to stop
def streamFrames(camera, videoSocket, stopEvent):
    while not stopEvent.is_set():
        ret, frame = camera.read() #reading the frame
        if not ret:
            #camera hiccup, wait briefly instead of spinning the CPU
            time.sleep(0.01)
            continue

        #frame = cv2.resize(frame, (1700,1024)) #optional frame resize to fit GUI

        #buffer is the new compressed .jpg
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
        if not ret:
            continue
        data = buffer.tobytes()

        #message size so that the server knows (header)
        msgSize = struct.pack("!I", len(data))
        videoSocket.sendall(msgSize + data)

#Background thread for one camera: keeps (re)connecting to the GUI and streams frames until stopEvent is set
def sendFrames(name, cameraIndex, serverIP, serverPort, stopEvent):
    camera = cv2.VideoCapture(cameraIndex)
    if not camera.isOpened():
        print(f"{name}: could not open camera {cameraIndex}, this stream is disabled")
        return

    try:
        #keeps reconnecting until told to stop, so the GUI can be started before or after the Pi
        while not stopEvent.is_set():
            try:
                mainSocket = socket.create_connection((serverIP, serverPort), timeout=5)
            except OSError:
                print(f"{name}: no receiver at {serverIP}:{serverPort}, retrying in {RETRY_DELAY}s")
                stopEvent.wait(RETRY_DELAY)
                continue

            print(f"{name}: streaming camera {cameraIndex} to {serverIP}:{serverPort}")
            try:
                streamFrames(camera, mainSocket, stopEvent)
            except OSError:
                print(f"{name}: receiver disconnected")
            finally:
                mainSocket.close()
    finally:
        #releasing the camera
        camera.release()
        print(f"{name}: stopped")

#Starts both camera streams in separate background threads
def startVideoStreams(serverIP, cameraIndexes, serverPorts):
    stopEvent = threading.Event()
    videoThreads = []

    for index, port in zip(cameraIndexes, serverPorts):
        videoThread = threading.Thread(
            target=sendFrames,
            args=(f"Video {len(videoThreads) + 1}", index, serverIP, port, stopEvent),
            daemon=True
        )
        videoThread.start()
        videoThreads.append(videoThread)

    return stopEvent, videoThreads
