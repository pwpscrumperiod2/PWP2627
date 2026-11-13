
# Tests the streaming

import cv2
import socket
import struct
import time

VIDEO_SERVER_IP = "127.0.0.1" # server address here
VIDEO_PORTS = (5002, 5003)
CAMERA_INDEX = 0
JPEG_QUALITY = 80
RETRY_DELAY = 2 # seconds

HEADER = struct.Struct("!I")


# Connects to one GUI receiver, retrying until it is available
def connectReceiver(serverIP, serverPort):
    while True:
        try:
            videoSocket = socket.create_connection((serverIP, serverPort), timeout=5)
            print(f"Connected to GUI at {serverIP}:{serverPort}")
            return videoSocket
        except OSError as error:
            print(f"Could not connect to {serverIP}:{serverPort}: {error}")
            print(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)


# Opens the camera once and sends each captured frame to both GUI connections
def testCamera():
    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        camera.release()
        raise RuntimeError(
            f"Could not open camera {CAMERA_INDEX}. "
            "Check the camera index and make sure no other program is using it."
        )

    videoSockets = [None] * len(VIDEO_PORTS)

    try:
        print(f"Camera {CAMERA_INDEX} opened. Press Ctrl+C to stop.")
        while True:
            # Connect/reconnect to each receiver independently
            for index, port in enumerate(VIDEO_PORTS):
                if videoSockets[index] is None:
                    videoSockets[index] = connectReceiver(VIDEO_SERVER_IP, port)

            # Capture one frame from the physical camera
            ret, frame = camera.read()
            if not ret or frame is None:
                print("Camera did not return a frame; trying again...")
                time.sleep(0.05)
                continue

            # Compress the frame once so both connections receive the same image
            ret, buffer = cv2.imencode(
                ".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
            )
            if not ret:
                continue

            data = buffer.tobytes()
            message = HEADER.pack(len(data)) + data

            # Send the same frame to both GUI streams
            for index, videoSocket in enumerate(videoSockets):
                try:
                    videoSocket.sendall(message)
                except OSError as error:
                    print(f"Stream {index + 1} disconnected: {error}")
                    videoSocket.close()
                    videoSockets[index] = None

    except KeyboardInterrupt:
        print("\nStopping camera test...")
    finally:
        for videoSocket in videoSockets:
            if videoSocket is not None:
                videoSocket.close()
        camera.release()
        print("Camera released and connections closed.")


if __name__ == "__main__":
    testCamera()
