import hashlib
from tkinter import messagebox
import sqlite3

def Auth(a, b, root):
    con = sqlite3.connect("User_Database.db")
    cur = con.cursor()

    if a == "" or b == "":
        messagebox.showerror("Error", "Please fill in all fields")
        return

    elif "!" in a or "@" in a or "#" in a or "$" in a or "%" in a or "^" in a or "&" in a or "*" in a or "(" in a or ")" in a:
        messagebox.showerror("Error", "Please enter a valid username without special characters")
        return

    else:
        hasheda = hashlib.sha256(a.encode()).hexdigest()
        hashedb = hashlib.sha256(b.encode()).hexdigest()
        cur.execute("""
        SELECT Password FROM users WHERE Username = ?
        """,
        (hasheda,)
        )
        row = cur.fetchone()
        con.close()
        if row == None:
            messagebox.showerror("Error", "Incorrect Username or Password. Create New Account?")
            return

        if row[0] != hashedb:
            messagebox.showerror("Error", "Incorrect Username or Password")
            return

        else:
            messagebox.showinfo("Success!", "Successfully logged in :)")
            for widget in root.winfo_children():
                widget.destroy()
            import MainGUI
            MainGUI.RunMainGUI(root)
            return
