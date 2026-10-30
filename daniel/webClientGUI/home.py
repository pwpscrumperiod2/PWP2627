import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Video Control System")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, False)

half_width = screen_width // 2
half_height = screen_height // 2


# Video 1
video1 = tk.Frame(root, bg="black")
video1.place(
   x=half_width * 0.05,
   y=half_height * 0.05,
   width=half_width * 0.9,
   height=half_height * 0.9
)

tk.Label(
   video1,
   text="VIDEO STREAM 1",
   font=("Arial", 24),
   fg="white",
   bg="black"
).place(relx=0.5, rely=0.5, anchor="center")


# Video 2
video2 = tk.Frame(root, bg="black")
video2.place(
   x=half_width * 0.05,
   y=half_height + half_height * 0.05,
   width=half_width * 0.9,
   height=half_height * 0.9
)

tk.Label(
   video2,
   text="VIDEO STREAM 2",
   font=("Arial", 24),
   fg="white",
   bg="black"
).place(relx=0.5, rely=0.5, anchor="center")


# Controls
controls = tk.Frame(root, bg="white")
controls.place(
   x=half_width,
   y=0,
   width=half_width,
   height=half_height
)

up_image = tk.PhotoImage(file="assets/up.png")
down_image = tk.PhotoImage(file="assets/down.png")
left_image = tk.PhotoImage(file="assets/left.png")
right_image = tk.PhotoImage(file="assets/right.png")
play_image = tk.PhotoImage(file="assets/play.png")
stop_image = tk.PhotoImage(file="assets/stop.png")

tk.Button(
   controls, image=up_image, width=40, height=40
).place(relx=0.5, rely=0.3, anchor="center")

tk.Button(
   controls, image=left_image, width=40, height=40
).place(relx=0.38, rely=0.5, anchor="center")

tk.Button(
   controls, image=play_image, width=40, height=40
).place(relx=0.46, rely=0.5, anchor="center")

tk.Button(
   controls, image=stop_image, width=40, height=40
).place(relx=0.54, rely=0.5, anchor="center")

tk.Button(
   controls, image=right_image, width=40, height=40
).place(relx=0.62, rely=0.5, anchor="center")

tk.Button(
   controls, image=down_image, width=40, height=40
).place(relx=0.5, rely=0.7, anchor="center")


# User log
log_frame = tk.Frame(root, bg="white")
log_frame.place(
   x=half_width,
   y=half_height,
   width=half_width,
   height=half_height
)

tk.Label(
   log_frame,
   text="USER LOG",
   font=("Arial", 22, "bold"),
   bg="white"
).pack(pady=10)

columns = ("user", "time", "status", "details")

log = ttk.Treeview(
   log_frame,
   columns=columns,
   show="headings"
)

for column in columns:
   log.heading(column, text=column)

log.column("user", width=100)
log.column("time", width=180)
log.column("status", width=120)
log.column("details", width=300)

log.insert(
   "",
   "end",
   values=("daniel", "23:59", "OK", "System initialized")
)

log.pack(
   fill="both",
   expand=True,
   padx=15,
   pady=10
)

root.mainloop()


