from tkinter import *
from tkinter import messagebox
import sqlite3

# Settings Window
def open_settings():
    settings_window = Toplevel() 
    settings_window.title("Settings")
    settings_window.configure(bg="white")
    settings_window.geometry("500x500")
    
    # Title Bar 
    title_bar = Frame(settings_window, width=500, height=60, bg="#f06d95") 
    title_bar.place(x=0, y=0)

    title = Label(title_bar, text="Settings", font=("Arial", 30, "bold"), bg="#f06d95", fg="white")
    title.place(x=180, y=10)
    
    # Patient Name
    patient_name_label = Label(settings_window, text="Patient Name:", font=("Arial", 14), bg="white")
    patient_name_label.place(x=50, y=100)
    patient_name = Entry(settings_window, font=("Arial", 14), bg="white", width=30)
    patient_name.place(x=200, y=100)
    
    # Age
    age_label = Label(settings_window, text="Age:", font=("Arial", 14), bg="white")
    age_label.place(x=50, y=140)
    age = Entry(settings_window, font=("Arial", 14), bg="white", width=30)
    age.place(x=200, y=140)
    
    # Phone Number
    phone_label = Label(settings_window, text="Phone No:", font=("Arial", 14), bg="white")
    phone_label.place(x=50, y=180)
    phone = Entry(settings_window, font=("Arial", 14), bg="white", width=30)
    phone.place(x=200, y=180)

    # Gender
    gender_label = Label(settings_window, text="Gender:", font=("Arial", 14), bg="white")
    gender_label.place(x=50, y=220)
    gender_options = ["Select Gender", "Male", "Female", "Other"]
    gender = StringVar()
    gender.set(gender_options[0]) 
    gender_menu = OptionMenu(settings_window, gender, *gender_options)
    gender_menu.config(font=("Arial", 14), bg="white")
    gender_menu.place(x=200, y=220)
 
    appointment_label = Label(settings_window, text="Make Appointment:", font=("Arial", 14), bg="white")
    appointment_label.place(x=50, y=260)
    
    appointment_var = IntVar() 
    appointment_check = Checkbutton(settings_window, text="Yes, I want to make an appointment", font=("Arial", 12), variable=appointment_var, bg="white")
    appointment_check.place(x=200, y=260)

    # Type of Appointment
    appointment_type_label = Label(settings_window, text="Appointment Type:", font=("Arial", 14), bg="white")
    appointment_type_label.place(x=50, y=300)
    appointment_type_options = ["General Consultation", "Specialist Consultation"]
    appointment_type = StringVar()
    appointment_type.set(appointment_type_options[0])  # Default value
    appointment_type_menu = OptionMenu(settings_window, appointment_type, *appointment_type_options)
    appointment_type_menu.config(font=("Arial", 14), bg="white")
    appointment_type_menu.place(x=200, y=300)
    
    time_label = Label(settings_window, text="Preferred Time:", font=("Arial", 14), bg="white")
    time_label.place(x=50, y=340)
    time_entry = Entry(settings_window, font=("Arial", 14), bg="white", width=30)
    time_entry.place(x=200, y=340)

    # Save Button to Save Settings
    def save_settings():
        name = patient_name.get()
        age_value = age.get()
        phone_value = phone.get()
        gender_value = gender.get()
        appointment_status = "Yes" if appointment_var.get() else "No"
        appointment_type_value = appointment_type.get()
        preferred_time = time_entry.get()
      
        conn = sqlite3.connect('user_settings.db')  
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            age INTEGER,
                            phone TEXT,
                            gender TEXT,
                            appointment_status TEXT,
                            appointment_type TEXT,
                            preferred_time TEXT)''')
      
        cursor.execute('''INSERT INTO settings (name, age, phone, gender, appointment_status, appointment_type, preferred_time) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                          (name, age_value, phone_value, gender_value, appointment_status, appointment_type_value, preferred_time))
        
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Settings", "Settings have been saved successfully!")

    # Save Button
    save_button = Button(settings_window, text="Save Settings", font=("Arial", 14), bg="#57a1f8", fg="white", command=save_settings)
    save_button.place(x=180, y=400)

    def on_closing():
        result = messagebox.askokcancel("Quit", "Do you want to close without saving changes?")
        if result:
            settings_window.destroy() 
        else:
            pass  

    settings_window.protocol("WM_DELETE_WINDOW", on_closing)

    
    settings_window.mainloop() 