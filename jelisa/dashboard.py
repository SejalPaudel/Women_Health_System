from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import runpy
from mentalhealth import open_mental_health

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

title = Label(title_bar, text="La Femme", font=("Arial", 30, "bold"), bg="#f06d95", fg="white")
title.place(x=170, y=45)

screen_width = project.winfo_screenwidth()
screen_height = project.winfo_screenheight()

# Minimize and Close button
def minimize_window():
    project.iconify()

def close_window():
    msg_box = messagebox.askquestion('Exit Application', 'Are you sure you want to close the application?',
                                     icon='warning')
    if msg_box == 'yes':
        project.destroy()

# Minimize Button (_)
btn_minimize = Button(title_bar, text="━", command=minimize_window, width=4, bg="#f06d95", fg="white",
                      border=0, font=("Arial", 12, "bold"))
btn_minimize.place(x=screen_width - 100, y=10)

# Close Button (X)
btn_close = Button(title_bar, text="✕", command=close_window, width=4, bg="#f06d95", fg="white",
                   border=0, font=("Arial", 12, "bold"))
btn_close.place(x=screen_width - 50, y=10)

#Back Button
def back():
    project.destroy()
    runpy.run_path("login.py") 

# Back Button ("<<")
btn_back = Button(project, text="<<", width=4, bg="#f06d95", border=0, font=("Arial", 14, "bold"), command=back)
btn_back.place(x=0, y=170)

def enter(i):
    btn_back['background'] = "red"

def leave(i):
    btn_back['background'] = "#f06d95"

btn_back.bind('<Enter>', enter)
btn_back.bind('<Leave>', leave)

#Logout Function
def logout():
    msg_box = messagebox.askquestion('Logout', 'Are you sure you want to log out?', icon='warning')
    if msg_box == 'yes':
        project.destroy() 
        runpy.run_path("login.py")  

#Dashboard Frame
frame_width = 450
frame_height = 445
frame2 = Frame(project, width=frame_width, height=frame_height, bg="white", highlightthickness=2)

frame2.place(x=(screen_width - frame_width) // 2, y=(screen_height - frame_height) // 3)

heading = Label(frame2, text='Dashboard', fg="#f06d95", bg="white", font=("Arial", 30))
heading.place(x=120, y=25)


Button(frame2,text="Mental Healthcare", width=20, pady=7,bg="#57a1f8", fg="white", border=0, command=open_mental_health ,
       font=("Arial", 14, "bold")).place(x=50, y=250)
project.protocol("WM_DELETE_WINDOW", close_window) 

project.mainloop()
