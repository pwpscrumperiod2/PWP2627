import socket
import threading

HOST = "127.0.0.1"
PORT = 8000
listening = True

print("\nWelcome to Terminal Chat Messenger 0.1 (Client)")
print("     Any incoming messages start with a |")
print("-----------------------------------------------\n")

def listener():
    global listening

    #sets timeout after no messages are sent after 30 secs
    sock.settimeout(1.0)

    while listening:
        try:
            data = sock.recv(1024)
            print(f"|{data.decode()}")

            if data.decode() == "Boop":
                listening == False
                break

            if not data:
                break
            if listening == False:
                break

        except socket.timeout: #shuts it off once hit timeout
            continue


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    try:
        sock.connect((HOST, PORT))

        print(f"You connected to {HOST} at port {PORT}.")
        print("Type anywhere to send a message\n")

        sock.sendall("Connected".encode())
        
        #background listener
        t = threading.Thread(target=listener)
        t.start()

        while listening:

            message = input("")
            if message == "quit":
                listening = False            
                sock.sendall("Boop".encode())
                sock.shutdown(socket.SHUT_RDWR) #shuts down connection
                t.join() #brings listener thread to foreground

                print("\nExiting...")
                break

            message = message.encode()

            try:
                sock.sendall(message)

            except ConnectionResetError:
                print("ConnectionResetError Inner")
                listening = False
                break

    #explicitly checks only if the server does not respond        
    except ConnectionRefusedError:
        print("Unable to connect to server.")
        listening = False

