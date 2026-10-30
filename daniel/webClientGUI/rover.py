#Communication with the RASPI library
import requests
import config

#IP address of the PI on the CS network
pi_url = f"http://{config.PI_IP}:{config.PI_PORT}"

def up():
    try:
        #Sends a JSON message to Raspi to Forward
        response = requests.post(
            f"{pi_url}/command",
            json={"action": "forward"},
            timeout=3
        )
        response.raise_for_status()

        #Reloads the page with a success message
        return "Successfully Moved Forward!"

    #Returns the error message
    except requests.RequestException:
        return "could not connect to raspberry pi"

#backward when the down button is clicked
def down():
    try:
        #Sends a JSON message to Raspi to Backward
        response = requests.post(
            f"{pi_url}/command",
            json={"action": "backward"},
            timeout=3
        )
        response.raise_for_status()

        #Reloads the page with a success message
        return "Successfully Moved Backward!"

    #Returns the error message
    except requests.RequestException:
        return "could not connect to raspberry pi"

#right when the right button is clicked
def right():
    try:
        #Sends a JSON message to Raspi to Right
        response = requests.post(
            f"{pi_url}/command",
            json={"action": "right"},
            timeout=3
        )
        response.raise_for_status()

        #Reloads the page with a success message
        return "Successfully Moved Right!"

    #Returns the error message
    except requests.RequestException:
        return "could not connect to raspberry pi"

#left when the left button is clicked
def left():
    try:
        #Sends a JSON message to Raspi to Left
        response = requests.post(
            f"{pi_url}/command",
            json={"action": "left"},
            timeout=3
        )
        response.raise_for_status()

        #Reloads the page with a success message
        return "Successfully Moved Left!"

    #Returns the error message
    except requests.RequestException:
        return "could not connect to raspberry pi"

#play when the play button is clicked
def play():
    try:
        #Sends a JSON message to Raspi to Play
        response = requests.post(
            f"{pi_url}/command",
            json={"action": "play"},
            timeout=3
        )
        response.raise_for_status()

        #Reloads the page with a success message
        return "Successfully Started!"

    #Returns the error message
    except requests.RequestException:
        return "could not connect to raspberry pi"

#stop when the stop button is clicked
def stop():
    try:
        #Sends a JSON message to Raspi to Stop
        response = requests.post(
            f"{pi_url}/command",
            json={"action": "stop"},
            timeout=3
        )
        response.raise_for_status()

        #Reloads the page with a success message
        return "Successfully Stopped!"

    #Returns the error message
    except requests.RequestException:
        return "could not connect to raspberry pi"
