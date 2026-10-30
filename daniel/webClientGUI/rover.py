#Communication with the RASPI library
from tkinter import messagebox
import requests
import config

#IP address of the PI on the CS network
pi_url = f"http://{config.PI_IP}:{config.PI_PORT}"

#forward when the up button is clicked
def up():
    try:
        #Sends a JSON message to Raspi to Forward
        response = requests.post(
            f"{pi_url}/command",
            json={"action": "forward"},
            timeout=3
        )
        response.raise_for_status()

        #Shows a popup with a success message
        messagebox.showinfo("Notification", "Successfully Moved Forward!")

    #Shows an error popup if the Pi could not be reached
    except requests.RequestException:
        messagebox.showinfo("Notification", "Could not connect to Raspberry Pi")

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

        #Shows a popup with a success message
        messagebox.showinfo("Notification", "Successfully Moved Backward!")
    #Shows an error popup if the Pi could not be reached
    except requests.RequestException:
        messagebox.showinfo("Notification", "Could not connect to Raspberry Pi")

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

        #Shows a popup with a success message
        messagebox.showinfo("Notification", "Successfully Moved Right!")

    #Shows an error popup if the Pi could not be reached
    except requests.RequestException:
        messagebox.showinfo("Notification", "Could not connect to Raspberry Pi")

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

        #Shows a popup with a success message
        messagebox.showinfo("Notification", "Successfully Moved Left!")

    #Shows an error popup if the Pi could not be reached
    except requests.RequestException:
        messagebox.showinfo("Notification", "Could not connect to Raspberry Pi")

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

        #Shows a popup with a success message
        messagebox.showinfo("Notification", "Successfully Started!")

    #Shows an error popup if the Pi could not be reached
    except requests.RequestException:
        messagebox.showinfo("Notification", "Could not connect to Raspberry Pi")

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

        #Shows a popup with a success message
        messagebox.showinfo("Notification", "Successfully Stopped!")

    #Shows an error popup if the Pi could not be reached
    except requests.RequestException:
        messagebox.showinfo("Notification", "Could not connect to Raspberry Pi")
