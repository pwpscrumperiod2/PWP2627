import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import rover

#install pillow, opencv,


main = tk.Tk()
main.geometry("1920x1080")
main.resizable(width=True, height=True)
main.title("none")


arrow_img=Image.open("arrow.png")


arrow_right_re=arrow_img.resize((150,150))
arrow_right=ImageTk.PhotoImage(arrow_right_re)


arrow_rotate_up=arrow_img.rotate(90, expand=True)
arrow_up_re=arrow_rotate_up.resize((150,150))
arrow_up=ImageTk.PhotoImage(arrow_up_re)


arrow_rotate_down=arrow_img.rotate(270, expand=True)
arrow_down_re=arrow_rotate_down.resize((150,150))
arrow_down=ImageTk.PhotoImage(arrow_down_re)


arrow_rotate_left=arrow_img.rotate(180, expand=True)
arrow_left_re=arrow_rotate_left.resize((150,150))
arrow_left=ImageTk.PhotoImage(arrow_left_re)


play_button_orig=Image.open("play_button.png")
re_play=play_button_orig.resize((150,150))
play_button_img=ImageTk.PhotoImage(re_play)
stop_button_orig=Image.open("stop_button.png")
re_stop=stop_button_orig.resize((150,150))
stop_button_img=ImageTk.PhotoImage(re_stop)


#upper left
q1 = Frame(main, width=960, height=540, relief="sunken")
q1.pack_propagate(False)
q1.grid(row=0, column=0, sticky="nsew")
placeholder1=Label(q1, text="Video Stream 1 Offline")
placeholder1.pack()


#upper right
q2 = Frame(main, width=960, height=540, bg="light gray")
q2.pack_propagate(False)
q2.grid(row=0, column=1, sticky="nsew")


up_button=Button(q2, image=arrow_up, command=rover.forward)
up_button.grid(row=0, column=3)
down_button=Button(q2, image=arrow_down, command=rover.backward)
down_button.grid(row=3, column=3)
left_button=Button(q2, image=arrow_left, command=rover.left)
left_button.grid(row=2, column=0)
right_button=Button(q2, image=arrow_right, command=rover.right)
right_button.grid(row=2, column=5)
play_button=Button(q2, image=play_button_img, command=rover.play)
play_button.grid(row=2, column=2)
stop_button=Button(q2, image=stop_button_img, command=rover.stop)
stop_button.grid(row=2, column=4)






#lower left
q3 = Frame(main, width=960, height=540, bg="light gray")
q3.pack_propagate(False)
q3.grid(row=1, column=0, sticky="nsew")
placeholder3=Label(q3, text="Video Stream 2 Offline")
placeholder3.pack()


#lower right
q4 = Frame(main, width=960, height=540, )
q4.pack_propagate(False)
q4.grid(row=1, column=1, sticky="nsew")


columns=("placeholder1", "placeholder2", "placeholder3")
user_log=ttk.Treeview(q4, columns=columns, show="headings")
user_log.heading("placeholder1", text="placeholder")
user_log.grid(column=0, row=0)


#placeholder4=Label(q4, text="placeholder4")
#placeholder4.pack()


main.grid_rowconfigure((0,1), weight=1)
main.grid_columnconfigure((0,1), weight=1)


main.mainloop()



