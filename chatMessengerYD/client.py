import socket
import threading

HOST = "127.0.0.1"
PORT = 8000
listening = True

def listener():
    global listening

    #sets timeout after no messages are sent after 30 secs
    sock.settimeout(1.0)

    while listening:
        try:
            data = sock.recv(1024)
            print(f"\nThem: {data.decode()}")

            if not data:
                break
            if listening == False:
                break

        except socket.timeout: #shuts it off once hit timeout
            continue

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    print(f"You connected to {HOST} at port {PORT}.")
    print("Type anywhere to send a message")

    sock.sendall("hiawef".encode())
    
    #background listener
    t = threading.Thread(target=listener)
    t.start()

    while True:

        message = input("")
        if message == "quit":
            listening = False            
            sock.sendall("They exited the chat.".encode())
            sock.shutdown(socket.SHUT_RDWR) #shuts down connection
            t.join() #brings listener thread to foreground

            print("\nExiting...")
            break

        message = message.encode()
        sock.sendall(message)

