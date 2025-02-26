from tkinter import *
from tkinter import messagebox
import sqlite3
from datetime import datetime

def open_mental_health():
    mental_health_window = Toplevel()
    mental_health_window.title("Mental Health Tracker")
    mental_health_window.configure(bg="#f5f5f5") 
    mental_health_window.geometry("650x600")
    
    # Title Bar
    title_bar = Frame(mental_health_window, width=700, height=60, bg="#f06d95")
    title_bar.place(x=0, y=0)

    title = Label(title_bar, text="Mental Health Tracker", font=("Arial", 30, "bold"), bg="#f06d95", fg="white")
    title.place(x=150, y=10)
    
    # Mood Tracking Section
    mood_label = Label(mental_health_window, text="How do you feel today?", font=("Arial", 14), bg="#f5f5f5", fg="#f06d95")
    mood_label.place(x=50, y=100)

    mood_options = ["Select Mood", "Very Happy", "Happy", "Neutral", "Sad", "Very Sad"]
    mood = StringVar()
    mood.set(mood_options[0])
    mood_menu = OptionMenu(mental_health_window, mood, *mood_options)
    mood_menu.config(font=("Arial", 14), bg="#ffffff", fg="#f06d95")
    mood_menu.place(x=250, y=100)

    #Anxiety & Stress Level
    anxiety_label = Label(mental_health_window, text="Anxiety Level (1-10):", font=("Arial", 14), bg="#f5f5f5", fg="#f06d95")
    anxiety_label.place(x=50, y=140)
    anxiety_level = Scale(mental_health_window, from_=1, to=10, orient=HORIZONTAL, font=("Arial", 14), bg="#ffffff", fg="#f06d95")
    anxiety_level.place(x=250, y=140)

    stress_label = Label(mental_health_window, text="Stress Level (1-10):", font=("Arial", 14), bg="#f5f5f5", fg="#f06d95")
    stress_label.place(x=50, y=180)
    stress_level = Scale(mental_health_window, from_=1, to=10, orient=HORIZONTAL, font=("Arial", 14), bg="#ffffff", fg="#f06d95")
    stress_level.place(x=250, y=180)

    #Symptoms & Triggers
    symptoms_label = Label(mental_health_window, text="Symptoms Today(optional):", font=("Arial", 14), bg="#f5f5f5", fg="#f06d95")
    symptoms_label.place(x=50, y=220)
    symptoms = Entry(mental_health_window, font=("Arial", 14), bg="#ffffff", fg="#f06d95", width=30)
    symptoms.place(x=300, y=220)
    
    triggers_label = Label(mental_health_window, text="Potential Triggers(optional):", font=("Arial", 14), bg="#f5f5f5", fg="#f06d95")
    triggers_label.place(x=50, y=260)
    triggers = Entry(mental_health_window, font=("Arial", 14), bg="#ffffff", fg="#f06d95", width=30)
    triggers.place(x=300, y=260)
    
    #Notes Section
    notes_label = Label(mental_health_window, text="Notes(optional):", font=("Arial", 14), bg="#f5f5f5", fg="#f06d95")
    notes_label.place(x=50, y=300)
    notes = Text(mental_health_window, font=("Arial", 14), bg="#ffffff", fg="#f06d95", width=30, height=5)
    notes.place(x=250, y=300)
    
    def save_mental_health():
        mood_value = mood.get()
        anxiety_value = anxiety_level.get()
        stress_value = stress_level.get()
        symptoms_value = symptoms.get()
        triggers_value = triggers.get()
        notes_value = notes.get("1.0", END).strip()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if mood_value == "Select Mood":
            messagebox.showerror("Input Error", "Please select your mood!")
            return
        
        conn = sqlite3.connect('mental_health.db') 
        cursor = conn.cursor()

    
        cursor.execute('''CREATE TABLE IF NOT EXISTS mental_health (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            mood TEXT,
                            anxiety_level INTEGER,
                            stress_level INTEGER,
                            symptoms TEXT,
                            triggers TEXT,
                            notes TEXT,
                            date TEXT)''')

        
        cursor.execute('''INSERT INTO mental_health (mood, anxiety_level, stress_level, symptoms, triggers, notes, date) 
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                          (mood_value, anxiety_value, stress_value, symptoms_value, triggers_value, notes_value, date))

        
        conn.commit()
        conn.close()

        
        messagebox.showinfo("Success", "Mental health data saved successfully!")

    # Save Button
    save_button = Button(mental_health_window, text="Save Mental Health Data", font=("Arial", 14), bg="#f06d95", fg="white",
                          command=save_mental_health)
    save_button.place(x=180, y=460)

    mental_health_window.mainloop()
