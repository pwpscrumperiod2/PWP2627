#Hello world
import socket
PORT = 8000
HOST = "127.0.0.1"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with sock as sock:
	sock.bind((HOST, PORT))
	sock.listen()
	conn, addr = sock.accept()
	with conn:
		print(f"Connected by {addr}")
		while True:
			data = conn.recv(1024)
			if not data:
				break
			message = input("You: ").encode()
			conn.sendall(message)
