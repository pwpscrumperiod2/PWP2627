#imports GUI library
import tkinter as tk
from tkinter import ttk
#imports the functions that send commands to the Raspberry Pi
import rover


#Set Up Tkinter Window
root = tk.Tk()
root.title("Video Control System")

#get the size of the user's screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#make the window fill the whole screen and stop it from being resized
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, False)

#the window is split into four quadrants, these are the size of one quadrant
half_width = screen_width // 2
half_height = screen_height // 2


# Video 1
#black box in the top left quadrant, with a 5% margin around it
video1 = tk.Frame(root, bg="black")
video1.place(x=half_width * 0.05, y=half_height * 0.05,width=half_width * 0.9, height=half_height * 0.9)
#placeholder text centered in the box until the video stream is added
tk.Label(video1, text="VIDEO STREAM 1", font=("Arial", 24), fg="white", bg="black").place(relx=0.5, rely=0.5, anchor="center")

# Video 2
#black box in the bottom left quadrant, with a 5% margin around it
video2 = tk.Frame(root, bg="black")
video2.place(x=half_width * 0.05, y=half_height + half_height * 0.05, width=half_width * 0.9, height=half_height * 0.9)
#placeholder text centered in the box until the video stream is added
tk.Label(video2, text="VIDEO STREAM 2", font=("Arial", 24), fg="white", bg="black").place(relx=0.5, rely=0.5, anchor="center")


# Controls
#panel in the top right quadrant that holds the rover control buttons
controls = tk.Frame(root, bg="white")
controls.place(x=half_width, y=0, width=half_width, height=half_height)

class guiButton():
   def __init__(self, name, image, command, relx, rely):
      self.name = name
      self.image = tk.PhotoImage(file=image)
      self.command = command
      self.relx = relx
      self.rely = rely
      #create the button and place it in the controls panel
      self.button = tk.Button(controls, image=self.image, width=40, height=40, command=self.command
      ).place(relx=self.relx, rely=self.rely, anchor="center")

guiButtons = [
   guiButton("up", "images/up.png", rover.up, 0.5, 0.3),
   guiButton("down", "images/down.png", rover.down, 0.5, 0.7),
   guiButton("left", "images/left.png", rover.left, 0.38, 0.5),
   guiButton("play", "images/play.png", rover.play, 0.46, 0.5),
   guiButton("stop", "images/stop.png", rover.stop, 0.54, 0.5),
   guiButton("right", "images/right.png", rover.right, 0.62, 0.5)
]   

# User log
#panel in the bottom right quadrant that shows a log of user activity
log_frame = tk.Frame(root, bg="white")
log_frame.place(x=half_width, y=half_height, width=half_width, height=half_height)

#title of the log panel
tk.Label(log_frame, text="USER LOG", font=("Arial", 22, "bold"), bg="white").pack(pady=10)

#names of the columns in the log table
columns = ("user", "time", "status", "details")

#table that holds the log entries, only showing the column headings (no tree column)
log = ttk.Treeview(log_frame, columns=columns, show="headings")

#label each column with its name
for column in columns:
   log.heading(column, text=column)

#set the width of each column in pixels
log.column("user", width=100)
log.column("time", width=180)
log.column("status", width=120)
log.column("details", width=300)

#example entry added at the end of the table
log.insert("", "end", values=("daniel", "23:59", "OK", "System initialized"))

#make the table fill the rest of the log panel
log.pack(fill="both",expand=True, padx=15, pady=10)

#Loop
root.mainloop()


