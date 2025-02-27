from tkinter import *
from tkinter import messagebox
import sqlite3

def open_medical_history():
    medical_history_window = Toplevel() 
    medical_history_window.title("Medical History")
    medical_history_window.configure(bg="white")
    medical_history_window.geometry("600x600")
    
    # Title Bar
    title_bar = Frame(medical_history_window, width=500, height=60, bg="#f06d95") 
    title_bar.place(x=0, y=0)
    title = Label(title_bar, text="Medical History", font=("Arial", 30, "bold"), bg="#f06d95", fg="white")
    title.place(x=120, y=10)
    
    # Patient Name
    patient_name_label = Label(medical_history_window, text="Patient Name:", font=("Arial", 14), bg="white")
    patient_name_label.place(x=50, y=100)
    patient_name = Entry(medical_history_window, font=("Arial", 14), bg="white", width=30)
    patient_name.place(x=200, y=100)
    
    # Age
    age_label = Label(medical_history_window, text="Age:", font=("Arial", 14), bg="white")
    age_label.place(x=50, y=140)
    age = Entry(medical_history_window, font=("Arial", 14), bg="white", width=30)
    age.place(x=200, y=140)
    
    # Gender
    gender_label = Label(medical_history_window, text="Gender:", font=("Arial", 14), bg="white")
    gender_label.place(x=50, y=180)
    gender_options = ["Select Gender", "Male", "Female", "Other"]
    gender = StringVar()
    gender.set(gender_options[0]) 
    gender_menu = OptionMenu(medical_history_window, gender, *gender_options)
    gender_menu.config(font=("Arial", 14), bg="white")
    gender_menu.place(x=200, y=180)
    
    # Medical Condition
    condition_label = Label(medical_history_window, text="Medical Condition:", font=("Arial", 14), bg="white")
    condition_label.place(x=50, y=220)
    condition = Entry(medical_history_window, font=("Arial", 14), bg="white", width=30)
    condition.place(x=200, y=220)

    # Medication
    medication_label = Label(medical_history_window, text="Medication:", font=("Arial", 14), bg="white")
    medication_label.place(x=50, y=260)
    medication = Entry(medical_history_window, font=("Arial", 14), bg="white", width=30)
    medication.place(x=200, y=260)

    # Allergies
    allergies_label = Label(medical_history_window, text="Allergies:", font=("Arial", 14), bg="white")
    allergies_label.place(x=50, y=300)
    allergies = Entry(medical_history_window, font=("Arial", 14), bg="white", width=30)
    allergies.place(x=200, y=300)

    # Reports
    reports_label = Label(medical_history_window, text="Reports:", font=("Arial", 14), bg="white")
    reports_label.place(x=50, y=340)
    reports = Text(medical_history_window, font=("Arial", 14), bg="white", width=30, height=5)
    reports.place(x=200, y=340)

    # Save Button to Save Medical History
    def save_medical_history():
        name = patient_name.get()
        age_value = age.get()
        gender_value = gender.get()
        condition_value = condition.get()
        medication_value = medication.get()
        allergies_value = allergies.get()
        reports_value = reports.get("1.0", END).strip()

        if not name or not age_value or not gender_value:
            messagebox.showerror("Input Error", "Name, Age, and Gender are required fields!")
            return

        conn = sqlite3.connect('medical_history.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS medical_history (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            age INTEGER,
                            gender TEXT,
                            condition TEXT,
                            medication TEXT,
                            allergies TEXT,
                            reports TEXT)''')

        cursor.execute('''INSERT INTO medical_history (name, age, gender, condition, medication, allergies, reports) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                          (name, age_value, gender_value, condition_value, medication_value, allergies_value, reports_value))

        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Medical History saved successfully!")

    # Save Button
    save_button = Button(medical_history_window, text="Save Medical History", font=("Arial", 14), bg="#57a1f8", fg="white", command=save_medical_history)
    save_button.place(x=180, y=460)

    def on_closing():
        result = messagebox.askokcancel("Quit", "Do you want to close without saving changes?")
        if result:
            medical_history_window.destroy() 
        else:
            pass 

    medical_history_window.protocol("WM_DELETE_WINDOW", on_closing)

    medical_history_window.mainloop()
