import socket

HOST = "127.0.0.1"
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:

        message = input("You: ")
        if message == "quit":
            break
        message = message.encode()

        sock.sendall(message)
        data = sock.recv(1024)
        print(f"Then: {data.decode()}")
