#https://medium.com/@staytechrich/socket-002-sending-and-receiving-video-over-sockets-cf701e4ef814

import socket
import cv2
import pickle
import struct
import time

def sendFrames(serverIP):
        mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mainSocket.connect((serverIP,5002)) #port 5002 5003 for video streaming

        camera = cv2.VideoCapture(0)

        try:
                while True:
                        ret, frame = camera.read() #reading the frame
                        #frame = cv2.resize(frame, (640, 480)) optional frame resize to fit GUI

                        #buffer is the new compressed .jpg
                        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                        data = pickle.dumps(buffer)

                        #message size so that the server knows (header)
                        msgSize = struct.pack("I", len(data))
                        mainSocket.sendall(msgSize + data)

        except KeyboardInterrupt:

                print("Exiting...")

        #releasing the camera, close socket, close windows
        camera.release()
        mainSocket.close

