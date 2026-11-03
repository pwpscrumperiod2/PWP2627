import tkinter
from tkinter import *
from tkinter import ttk
import PIL
from PIL import *
from PIL import Image, ImageTk
from robot_commands import SendCommand

def RunMainGUI(root):
    #making the window

    root.title("Robot GUI")
    root.geometry("1920x1080")
    root.columnconfigure(0, weight=1, uniform="column")
    root.columnconfigure(1, weight=1, uniform="column")
    root.rowconfigure(0, weight=1, uniform="row")
    root.rowconfigure(1, weight=1, uniform="row")

    # top left quadrant
    TL = ttk.Frame(root, width=900, height=540, borderwidth= 5, relief= "sunken")
    TL.grid(row=0, column=0,sticky="nsew")
    TL.grid_propagate(False)
    Placehold1 = Label(TL, text="Video Placeholder")
    Placehold1.pack()

    # bottom left quadrant
    BL = ttk.Frame(root, width=900, height=540, borderwidth= 5, relief= "sunken")
    BL.grid(row=1, column=0,sticky="nsew")
    BL.grid_propagate(False)
    Placehold2 = Label(BL, text="Video Placeholder")
    Placehold2.pack()

    # top right quadrant
    TR = ttk.Frame(root, width=900, height=540, borderwidth= 5, relief= "sunken")
    TR.grid(row=0, column=1, sticky="nsew")
    TR.grid_propagate(False)
    TR.columnconfigure(0, weight=1)

    #arrow keys
    arrows = Image.open("Assets/Original_Arrow.png").convert("RGBA")
    resized = arrows.resize((50,50))

    Controls = Frame(TR)
    Controls.place(relx=0.5, rely=0.5, anchor=CENTER)

    resizedup = resized.rotate(90)
    resizedup.save("Assets/Upbutton.png")
    uparrow = ImageTk.PhotoImage(resizedup)
    Up = Button(Controls, image = uparrow,width= 100,command=lambda: SendCommand("forward"))
    Up.grid(row=0, column=2, sticky="nsew")

    resizeddown = resized.rotate(270)
    resizeddown.save("Assets/Downbutton.png")
    downarrow = ImageTk.PhotoImage(resizeddown)
    Down = Button(Controls, image = downarrow,width= 100,command=lambda: SendCommand("backward"))
    Down.grid(row=1, column=2)

    resizedleft = resized.rotate(180)
    resizedleft.save("Assets/Leftbutton.png")
    Leftarrow = ImageTk.PhotoImage(resizedleft)
    Left = Button(Controls, image = Leftarrow,width= 100,command=lambda: SendCommand("left"))
    Left.grid(row=1, column=1)

    resizedright = resized.rotate(0)
    resizedright.save("Assets/Rightbutton.png")
    rightarrow = ImageTk.PhotoImage(resizedright)
    Right = Button(Controls, image = rightarrow,width= 100,command=lambda: SendCommand("right"))
    Right.grid(row=1, column=3)

    #start/stop button
    playbutton = Image.open("Assets/Play.png")
    resizedplay = playbutton.resize((50,50))
    finalplaybutton = ImageTk.PhotoImage(resizedplay)
    play = Button(Controls, image = finalplaybutton,width= 100,command=lambda: SendCommand("play"))
    play.grid(row=2, column=1)

    pausebutton = Image.open("Assets/Pause.png")
    resizedpause = pausebutton.resize((50,50))
    finalpausebutton = ImageTk.PhotoImage(resizedpause)
    pause = Button(Controls, image = finalpausebutton,width= 100,command=lambda: SendCommand("stop"))
    pause.grid(row=2, column=2)

    # bottom right quadrant
    BR = ttk.Frame(root, width=900, height=540, borderwidth= 5, relief= "sunken")
    BR.grid(row=1, column=1, sticky="nsew")
    BR.grid_propagate(False)
    Userlog = Label(BR, text="User Log")
    Userlog.grid(row=0, column=0, padx=250)
    User = Label(BR, text="User")
    User.grid(row=1, column=1)
    Date = Label(BR, text="Date")
    Date.grid(row=1, column=2)
    Time = Label(BR, text="Time")
    Time.grid(row=1, column=3)

    root.uparrow = uparrow
    root.downarrow = downarrow
    root.leftarrow = Leftarrow
    root.rightarrow = rightarrow
    root.finalplaybutton = finalplaybutton
    root.finalpausebutton = finalpausebutton