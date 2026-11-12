import socket
import cv2
import pickle
import struct

def receiveFrames(host='0.0.0.0', port=5002):
    # Setup socket server
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    serverSocket.listen(1)
    print(f"Listening for video stream on port {port}...")

    conn, addr = serverSocket.accept()
    print(f"Connection established with: {addr}")

    data = b""
    payload_size = struct.calcsize("I")

    try:
        while True:
            # 1. Read the header to get the exact size of the incoming frame payload
            while len(data) < payload_size:
                packet = conn.recv(4 * 1024)  # 4KB buffer chunk
                if not packet:
                    break
                data += packet
            
            if len(data) < payload_size:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("I", packed_msg_size)[0]

            # 2. Read the actual frame data until we have the full message size
            while len(data) < msg_size:
                packet = conn.recv(4 * 1024)
                if not packet:
                    break
                data += packet
            
            if len(data) < msg_size:
                break

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # 3. Unpickle and decode the frame
            frame_buffer = pickle.loads(frame_data)
            frame = cv2.imdecode(frame_buffer, cv2.IMREAD_COLOR)

            # 4. Display the frame
            if frame is not None:
                cv2.imshow('Video Receiver', frame)

            # Press 'q' to exit the video window safely
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        conn.close()
        serverSocket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    receiveFrames()
