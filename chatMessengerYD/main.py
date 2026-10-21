#imports sockets and threading for background running
import socket
import threading

#points to port and host
#because this is server side, HOST is '' because it is listening for a connection, not 
#making one
PORT = 8000
HOST = ""
serverRunning = True

print("\nWelcome to Terminal Chat Messenger 0.1 (Server)")
print("    Any incoming messages start with a |")
print("----------------------------------------------\n")

#same function from the client side
def listener():
    global serverRunning

    #sets timeout for one second, so that every one second, it restarts the listening
    sock.settimeout(1.0)

    while listening:
        try:
            #recieves the data, decodes it from binary format, and prints it
            data = sock.recv(1024)
            print(f"| {data.decode()}")

            if data.decode() == "Boop":
                print("The other person closed the connection.")
                serverRunning = False
                break

            if not data:
                serverRunning = False
                break

            if serverRunning == False:
                break

        except socket.timeout: #shuts it off once hit timeout
            continue

        except OSError: #for the issue on line 26, when it tries to access a sock that doesn't exist
            print("Connection Closed.")

listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with listeningSocket as listeningSocket:
    listeningSocket.bind((HOST, PORT))
    listeningSocket.listen()

    while serverRunning: 
        listening = True
        sock, addr = listeningSocket.accept()
            
        #starts the listener function
        t = threading.Thread(target=listener)
        t.start()

        #opens the connection
        #this is the actual server-client connection, when it exits this socket closes
        #on a real persistent server you would not close the (other) listening socket and instead leave it open
        with sock:
            print(f"{addr[0]} connected to the server on port {addr[1]}.\n")

            #the actual input loop, where it allows you to type
            while listening:

                message = input("")
                if message == "quit":
                    listening = False
                    sock.sendall("Boop".encode())

                    print("\nExiting...")
                    break

                message = message.encode()
                sock.sendall(message)

            break
