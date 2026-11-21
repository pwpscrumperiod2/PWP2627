#communicates any errors or successes to the user 
from tkinter import messagebox
#communicates to raspi
import requests
#imports the config file that holds the IP address of the Raspi
import config

#IP address of the PI on the CS network
pi_url = f"http://{config.PI_IP}:{config.PI_PORT}"

#Sends a command to the Raspi and shows a popup with the result
def send_command(action, success_msg):
    try:
        #Sends a JSON message to Raspi with the given action
        response = requests.post(
            f"{pi_url}/command",
            json={"action": action},
            timeout=3
        )
        response.raise_for_status()

        #Shows a popup with a success message
        messagebox.showinfo("Notification", success_msg)

    #Shows an error popup if the Pi could not be reached
    except requests.RequestException:
        messagebox.showinfo("Notification", f"{action} could not connect to Raspberry Pi")

#One function per button, each calls send_command with the appropriate action and success message
def up():    send_command("forward",  "Successfully Moved Forward!")
def down():  send_command("backward", "Successfully Moved Backward!")
def left():  send_command("left",     "Successfully Moved Left!")
def right(): send_command("right",    "Successfully Moved Right!")
def play():  send_command("play",     "Successfully Started!")
def stop():  send_command("stop",     "Successfully Stopped!")
