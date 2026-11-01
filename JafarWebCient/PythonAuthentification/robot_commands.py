#Web application library
from flask import jsonify, redirect, render_template, request
#Communication with the RASPI library
import requests
#imports the private settings
import config
#display errors
from tkinter import messagebox

#IP address of the PI on the CS network
pi_url = f"http://{config.PI_IP}:{config.PI_PORT}"

#Create a function to send commands to the raspberry pi
def SendCommand(action):
    try:
        #Sends a JSON message to Raspi to Forward
        response = requests.post(
            f"{pi_url}/command",
            json={"action": action},
            timeout=3
        )
        response.raise_for_status()

        #Success Message
        print(f"Successfully sent command: {action}")

    #Returns the error message
    except requests.RequestException:
        messagebox.showerror("Connection Error", "Could not connect to Raspberry Pi")

