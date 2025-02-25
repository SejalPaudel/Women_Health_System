from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import tkinter.font as font
import runpy
import sqlite3
import hashlib  # ✅ For SHA-256 password hashing

# Create the main project window
project = Tk()
project.configure(bg="white")
project.attributes("-fullscreen", True)

logo = Image.open("logo.jpeg")
logo = logo.resize((140, 150))
logo_image = ImageTk.PhotoImage(logo)

# Title Bar
title_bar = Frame(project, width=1550, height=160, bg="#f06d95")
title_bar.place(x=0, y=0)

logo_label = Label(title_bar, image=logo_image, bg="#f06d95")
logo_label.place(x=10, y=10)

title = Label(title_bar, text="La Femme", font=("Arial", 40, "bold"), bg="#f06d95", fg="white")
title.place(x=170, y=45)

screen_width = project.winfo_screenwidth()
screen_height = project.winfo_screenheight()

# Close window functions
def minimize_window():
    project.iconify()

def close_window():
    if messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?', icon='warning') == 'yes':
        project.destroy()

btn_minimize = Button(title_bar, text="━", command=minimize_window, width=4, bg="#f06d95", fg="white",
                      border=0, font=("Arial", 12, "bold"))
btn_minimize.place(x=screen_width - 100, y=10)

btn_close = Button(title_bar, text="✕", command=close_window, width=4, bg="#f06d95", fg="white",
                   border=0, font=("Arial", 12, "bold"))
btn_close.place(x=screen_width - 50, y=10)

# Back Button
def back():
    project.destroy()
    runpy.run_path("s.py")

btn_back = Button(project, text="<<", width=4, bg="#f06d95", border=0, font=("Arial", 14, "bold"), command=back)
btn_back.place(x=0, y=170)

def enter(i):
    btn_back['background'] = "red"

def leave(i):
    btn_back['background'] = "#f06d95"

btn_back.bind('<Enter>', enter)
btn_back.bind('<Leave>', leave)

# --- Sign In Frame ---
frame_width = 450
frame_height = 455
frame2 = Frame(project, width=frame_width, height=frame_height, bg="white", highlightthickness=2, highlightbackground="#f06d95")
frame2.place(x=(screen_width - frame_width) // 2, y=(screen_height - frame_height) // 2 + 50)

heading = Label(frame2, text='Sign In', fg="#f06d95", bg="white", font=("Arial", 30, "bold"))
heading.place(x=160, y=25)

# Placeholder handling for email
def on_enter(w):
    if user.get() == "Email":
        user.delete(0, "end")

def on_leave(w):
    if user.get() == "":
        user.insert(0, "Email")

user = Entry(frame2, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 16))
user.place(x=50, y=125)
user.insert(0, "Email")
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame2, width=340, height=2, bg="#f06d95").place(x=50, y=152)

# Password Entry
def on_enter_password(w):
    if code.get() == "Password":
        code.delete(0, "end")
        code.config(show="●")

def on_leave_password(w):
    if code.get() == "":
        code.config(show="")
        code.insert(0, "Password")

code = Entry(frame2, show="*", width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 16))
code.place(x=50, y=200)
code.insert(0, "Password")
code.bind('<FocusIn>', on_enter_password)
code.bind('<FocusOut>', on_leave_password)

Frame(frame2, width=340, height=2, bg="#f06d95").place(x=50, y=227)

# ✅ Hashing function (same as signup)
def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def signin():
    email_input = user.get().strip()
    password_input = code.get().strip()

    if email_input == "" or password_input == "":
        messagebox.showwarning("Input Error", "Please fill in both fields.")
        return

    try:
        conn = sqlite3.connect("signup.db")
        cursor = conn.cursor()

        
        hashed_password = hash_password(password_input)
        cursor.execute("SELECT * FROM patient WHERE LOWER(email)=? AND password=?", (email_input.lower(), hashed_password))
        user_data = cursor.fetchone()

        if user_data:
            messagebox.showinfo("Login Successful", "Welcome to La Femme!")
            project.destroy()
            runpy.run_path("dash.py")
        else:
            messagebox.showerror("Error", "Invalid email or password.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
    finally:
        conn.close()

# Sign In Button
Button(frame2, width=30, pady=10, text="Sign In", bg="#f06d95", fg="white", border=0,
       command=signin, font=("Arial", 14, "bold")).place(x=35, y=300)


def initialize_database():
    conn = sqlite3.connect("signup.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        patient_id TEXT NOT NULL UNIQUE,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

initialize_database()
project.mainloop()
