import hashlib
import sqlite3
from tkinter import messagebox

def CreateAcc(a, b, c, Loginpage):
    con = sqlite3.connect("User_Database.db")
    cur = con.cursor()

    if a == "":
        messagebox.showerror("Error", "Please enter a valid username")
        return

    elif "!" in a or "@" in a or "#" in a or "$" in a or "%" in a or "^" in a or "&" in a or "*" in a or "(" in a or ")" in a:
        messagebox.showerror("Error", "Please enter a valid username without special characters")
        return

    elif b != c:
        messagebox.showerror("Error", "Passwords do not match")
        return
    else:
        hasheda = hashlib.sha256(a.encode()).hexdigest()
        hashedb = hashlib.sha256(b.encode()).hexdigest()
        try:
            cur.execute("""
            INSERT INTO users (Username, Password)
            VALUES (?, ?)
            """,
            (hasheda, hashedb)
            )
            con.commit()
            con.close()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
            return

        messagebox.showinfo("Success!", "Successfully made a new account :)")
        Loginpage()
