import requests
import config
from tkinter import messagebox

#IP address of the PI on the CS network
pi_url = f"http://{config.PI_IP}:{config.PI_PORT}"


#forward when the up button is clicked
def forward():
  try:
    #Sends a JSON message to Raspi to Forward
    response = requests.post(
      f"{pi_url}/command",
      json={"action": "forward"},
      timeout=3
    )
    response.raise_for_status()
    
  #Informs user if there was a connection error with the raspPI
  except requests.RequestException:
    messagebox.showinfo("Message", "ERROR: could not connect to the raspberry PI")

#backward when the down button is clicked
def backward():
  try:
    #Sends a JSON message to Raspi to Backward
    response = requests.post(
      f"{pi_url}/command",
      json={"action": "backward"},
      timeout=3
    )
    response.raise_for_status()
  
  #Informs user if there was a connection error with the raspPI
  except requests.RequestException:
    messagebox.showinfo("Message", "ERROR: could not connect to the raspberry PI")

#turn right when right button is clicked
def right():
  try:
    #Sends a JSON message to Raspi to Right
    response = requests.post(
      f"{pi_url}/command",
      json={"action": "right"},
      timeout=3
    )
    response.raise_for_status()

  #Informs user if there was a connection error with the raspPI
  except requests.RequestException:
    messagebox.showinfo("Message", "ERROR: could not connect to the raspberry PI")

#turn left when left button is clicked
def left():
  try:
    #Sends a JSON message to Raspi to Left
    response = requests.post(
      f"{pi_url}/command",
      json={"action": "left"},
      timeout=3
    )
    response.raise_for_status()
  
  #Informs user if there was a connection error with the raspPI
  except requests.RequestException:
    messagebox.showinfo("Message", "ERROR: could not connect to the raspberry PI")

#Run play when green play button is clicked
def play():
  try:
    #Sends a JSON message to Raspi to Play
    response = requests.post(
      f"{pi_url}/command",
      json={"action": "play"},
      timeout=3
    )
    response.raise_for_status()
  
  #Informs user if there was a connection error with the raspPI
  except requests.RequestException:
    messagebox.showinfo("Message", "ERROR: could not connect to the raspberry PI")

#stop when stop button is clicked
def stop():
  try:
    #Sends a JSON message to Raspi to Stop
    response = requests.post(
      f"{pi_url}/command",
      json={"action": "stop"},
      timeout=3
    )
    response.raise_for_status()
  
  #Informs user if there was an error connectiong to the raspberry PI")
  except requests.RequestException:
    messagebox.showinfo("Message", "ERROR: could not connect to the raspberry PI")
