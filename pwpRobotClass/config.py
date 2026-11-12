#Settings for the web application

#Key flask uses to sign session cookies
SECRET_KEY = "borat"

#IP address and port of the PI on the CS network
PI_IP = "192.168.240.247"
PI_PORT = 5001

#Ports this computer listens on for the Pi's two camera streams, one pipe each
#(must match VIDEO_PORT_1 / VIDEO_PORT_2 in raspiFiles/remote.py)
VIDEO_PORT_1 = 5002
VIDEO_PORT_2 = 5003
