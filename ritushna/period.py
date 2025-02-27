import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

# Function to open the period tracker window
def open_period_tracker():
    tracker_window = tk.Toplevel()
    tracker_window.title("Period Tracker")
    tracker_window.geometry("600x500")
    tracker_window.configure(bg="white")
    
    # Title Bar
    title_bar = tk.Frame(tracker_window, width=800, height=60, bg="#f06d95")
    title_bar.place(x=0, y=0)
    title = tk.Label(title_bar, text="Period Tracker", font=("Arial", 30, "bold"), bg="#f06d95", fg="white")
    title.place(x=250, y=10)

    # Period Start and End Date
    start_date_label = tk.Label(tracker_window, text="Period Start Date:", font=("Arial", 14), bg="white")
    start_date_label.place(x=50, y=100)
    start_date_entry = tk.Entry(tracker_window, font=("Arial", 14), bg="white", width=30)
    start_date_entry.place(x=260, y=100)
    
    end_date_label = tk.Label(tracker_window, text="Period End Date:", font=("Arial", 14), bg="white")
    end_date_label.place(x=50, y=140)
    end_date_entry = tk.Entry(tracker_window, font=("Arial", 14), bg="white", width=30)
    end_date_entry.place(x=260, y=140)
    
    # Symptoms Entry
    symptoms_label = tk.Label(tracker_window, text="Symptoms(Optional):", font=("Arial", 14), bg="white")
    symptoms_label.place(x=50, y=180)
    symptoms_entry = tk.Entry(tracker_window, font=("Arial", 14), bg="white", width=30)
    symptoms_entry.place(x=260, y=180)

    # Save Button to Save Period Data
    def save_period_data():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        symptoms = symptoms_entry.get()

        if not start_date or not end_date:
            messagebox.showerror("Error", "Start and End Date are required!")
            return

        try:
            # Parse date inputs
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            cycle_length = (end_date_obj - start_date_obj).days

            # Save data to SQLite
            conn = sqlite3.connect('period_tracker.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS period_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                start_date TEXT,
                                end_date TEXT,
                                cycle_length INTEGER,
                                symptoms TEXT)''')

            cursor.execute('''INSERT INTO period_data (start_date, end_date, cycle_length, symptoms) 
                              VALUES (?, ?, ?, ?)''', 
                              (start_date, end_date, cycle_length, symptoms))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Period data saved successfully!")

        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Please use YYYY-MM-DD")

    save_button = tk.Button(tracker_window, text="Save Period Data", font=("Arial", 14), bg="#57a1f8", fg="white", command=save_period_data)
    save_button.place(x=250, y=220)

    tracker_window.mainloop()

