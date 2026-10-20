# Hello world
import socket
PORT = 8000
HOST = ""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with sock as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    while True:
        conn, addr = sock.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                message = input("You: ").encode()
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(message)
                print(f"Them: {data.decode()}")
