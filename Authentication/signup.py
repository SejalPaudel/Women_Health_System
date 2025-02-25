from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import hashlib
import runpy

project = Tk()
project.configure(bg="white")
project.attributes("-fullscreen", True)

# Logo
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

# Window Controls
def min_window():
    project.iconify()

def close_window():
    if messagebox.askquestion('Exit Application', 'Are you sure you want to close?', icon='warning') == 'yes':
        project.destroy()

btn_min = Button(title_bar, text="━", command=min_window, width=4, bg="#f06d95", fg="white", border=0, font=("Arial", 12, "bold"))
btn_min.place(x=screen_width - 100, y=10)

btn_close = Button(title_bar, text="✕", command=close_window, width=4, bg="#f06d95", fg="white", border=0, font=("Arial", 12, "bold"))
btn_close.place(x=screen_width - 50, y=10)

# Frame for Sign-up and Sign-in
frame = Frame(project, width=500, height=600, bg="white", highlightthickness=2, highlightbackground="#f06d95")
frame.place(x=(screen_width - 500) // 2, y=(screen_height - 600) // 2 + 80)

heading = Label(frame, text='Sign Up', fg="#f06d95", bg="white", font=("Arial", 30))
heading.place(x=180, y=10)

def create_entry(frame, x, y, width, placeholder, show=None):
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, END)
            entry.config(show=show if show else "")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(show="")

    entry = Entry(frame, width=width, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 16))
    entry.place(x=x, y=y)
    entry.insert(0, placeholder)
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)
    Frame(frame, width=360, height=2, bg="#f06d95").place(x=x, y=y + 27)
    return entry

# Form fields
name = create_entry(frame, 42, 85, 25, "Name")
patient_id = create_entry(frame, 42, 150, 25, "Patient ID")
phone_number = create_entry(frame, 42, 215, 25, "Phone Number")
email = create_entry(frame, 42, 280, 25, "Enter Your Email")
password = create_entry(frame, 42, 345, 25, "Create Password", show="●")
confirm_password = create_entry(frame, 42, 410, 25, "Confirm Password", show="●")

# Database setup
conn = sqlite3.connect('signup.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    patient_id TEXT NOT NULL UNIQUE,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)""")
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup():
    u_name = name.get()
    p_id = patient_id.get()
    p_phone = phone_number.get()
    p_email = email.get()
    p_password = password.get()
    c_password = confirm_password.get()

    if not all([u_name, p_id, p_phone, p_email, p_password, c_password]):
        messagebox.showinfo("Error", "Please fill all fields.")
    elif not p_id.isdigit():
        messagebox.showerror("Error", "Patient ID must be numeric.")
    elif not p_phone.isdigit() or len(p_phone) != 10:
        messagebox.showerror("Error", "Enter a valid 10-digit phone number.")
    elif "@" not in p_email or not p_email.endswith(".com"):
        messagebox.showerror("Error", "Enter a valid email.")
    elif p_password != c_password:
        messagebox.showerror("Error", "Passwords do not match.")
    else:
        try:
            hashed_password = hash_password(p_password)
            c.execute("INSERT INTO patient (name, patient_id, phone_number, email, password) VALUES (?, ?, ?, ?, ?)",
                      (u_name, p_id, p_phone, p_email, hashed_password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful.")
            go_to_login()
        except sqlite3.IntegrityError as e:
            messagebox.showinfo("Error", "Patient ID or Email already exists.")
            print(e)

def go_to_login():
    project.destroy()
    runpy.run_path("login.py")

signup_btn = Button(frame, width=39, pady=7, text="Sign Up", bg="#f06d95", fg="white", border=0, cursor="hand2",
                    font=("Arial", 13), command=signup)
signup_btn.place(x=40, y=480)

login_btn = Button(frame, width=39, pady=7, text="Sign In", bg="#f06d95", fg="white", border=0, cursor="hand2",
                   font=("Arial", 13), command=go_to_login)
login_btn.place(x=40, y=530)


project.mainloop()

conn.close()
