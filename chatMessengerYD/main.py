#imports sockets and threading for background running
import socket
import threading

#points to port and host
#because this is server side, HOST is '' because it is listening for a connection, not 
#making one
PORT = 8000
HOST = ""
listening = True

#same function from the client side
def listener():
    global listening

    #sets timeout for one second, so that every one second, it restarts the listening
    listeningSocket.settimeout(1.0)

    while listening:
        try:
            #recieves the data, decodes it from binary format, and prints it
            data = sock.recv(1024)
            print(f"\nThem: {data.decode()}")

            if not data:
                break
            if listening == False:
                break

        except socket.timeout: #shuts it off once hit timeout
            continue

listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with listeningSocket as listeningSocket:
    listeningSocket.bind((HOST, PORT))
    listeningSocket.listen()

    while True:
        sock, addr = listeningSocket.accept()
            
        #starts the listener function
        t = threading.Thread(target=listener)
        t.start()

        #opens the connection
        with sock:
            print(f"Connected by {addr}")

            #the actual input loop, where it allows you to type
            while True:

                message = input("You: ")
                if message == "quit":
                    listening = False
                    sock.sendall("They exited the chat.".encode())
                    sock.shutdown(socket.SHUT_RDWR) #shuts down the connection

                    t.join() #brings the thread to the foreground
                    print("\nExiting...")
                    break

                message = message.encode()

                sock.sendall(message)
