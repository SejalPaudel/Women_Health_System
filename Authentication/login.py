from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import runpy
import sqlite3
import hashlib  

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

#Sign In Frame
frame_width = 450
frame_height = 455
frame2 = Frame(project, width=frame_width, height=frame_height, bg="white", highlightthickness=2, highlightbackground="#f06d95")
frame2.place(x=(screen_width - frame_width) // 2, y=(screen_height - frame_height) // 2 + 50)

heading = Label(frame2, text='Sign In', fg="#f06d95", bg="white", font=("Arial", 30, "bold"))
heading.place(x=160, y=25)

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

def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# Function to show password
def password_visibile():
    if show_password_var.get():
        code.config(show='')  # Show password
    else:
        code.config(show='●')  # Hide password

show_password_var = IntVar()

show_password_cb = Checkbutton(
    frame2, text="Show Password", variable=show_password_var,
    bg="white", font=("Microsoft Yahei UI Light", 12),
    command=password_visibile
)
show_password_cb.place(x=50, y=240)


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
       
#Forgot Password
def forgot_password():
    def validate_email_exists(email):
        """Validates if the email exists in the database."""
        conn = sqlite3.connect("signup.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patient WHERE LOWER(email)=?", (email.lower(),))
        user_data = cursor.fetchone()
        conn.close()
        return user_data

    def reset_password():
        email = email_entry.get().strip()
        if not email:
            messagebox.showwarning("Input Error", "Please enter an email address.")
            return
        
        user_data = validate_email_exists(email)
        
        if user_data:
            reset_window = Toplevel(project)
            reset_window.title("Reset Password")
            reset_window.geometry("400x250")

            new_password_label = Label(reset_window, text="Enter New Password:", font=("Arial", 14))
            new_password_label.pack(pady=20)
            
            new_password_entry = Entry(reset_window, show="*", width=25, font=("Arial", 14))
            new_password_entry.pack(pady=10)

            def save_new_password():
                new_password = new_password_entry.get().strip()
                if not new_password:
                    messagebox.showwarning("Input Error", "Please enter a new password.")
                    return
                hashed_password = hash_password(new_password)
                
                # Update the password in the database
                conn = sqlite3.connect("signup.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE patient SET password=? WHERE LOWER(email)=?", (hashed_password, email.lower()))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Password Reset", "Your password has been reset successfully.")
                reset_window.destroy()

            reset_button = Button(reset_window, text="Reset Password", command=save_new_password, bg="#f06d95", fg="white")
            reset_button.pack(pady=10)

        else:
            messagebox.showerror("Email Not Found", "No account found with this email.")

    # Forgot Password Window
    forgot_window = Toplevel(project)
    forgot_window.title("Forgot Password")
    forgot_window.geometry("400x250")
    
    forgot_label = Label(forgot_window, text="Enter your email to reset password:", font=("Arial", 14))
    forgot_label.pack(pady=20)

    email_entry = Entry(forgot_window, width=25, font=("Arial", 14))
    email_entry.pack(pady=10)

    reset_button = Button(forgot_window, text="Submit", command=reset_password, bg="#f06d95", fg="white")
    reset_button.pack(pady=10)

# Forgot Password Button
Button(frame2, width=30, pady=5, text="Forgot Password?", bg="#f06d95", fg="white", border=0,
       command=forgot_password, font=("Arial", 12, "bold")).place(x=35, y=370)


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
