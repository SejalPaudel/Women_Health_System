from tkinter import *
from tkinter import messagebox
import sqlite3

def open_user_details():
    user_window = Toplevel()
    user_window.title("User Details")
    user_window.geometry("600x500")
    user_window.configure(bg="white")
    
    # Title Bar
    title_bar = Frame(user_window, width=600, height=100, bg="#f06d95")
    title_bar.pack(side=TOP, fill=X)

    title_label = Label(title_bar, text="Manage Users", font=("Arial", 30, "bold"), bg="#f06d95", fg="white")
    title_label.place(x=180, y=25)

    def fetch_user_data():
        user_id = patient_id.get().strip()
        
        if not user_id.isdigit():
            messagebox.showerror("Invalid ID", "Please enter a valid patient ID.")
            return
        
        try:
            conn = sqlite3.connect("signup.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patient WHERE patient_id=?", (user_id,))
            user_data = cursor.fetchone()
            
            if user_data:
                name_entry.delete(0, END)
                name_entry.insert(0, user_data[1])  # Name
                
                phone_entry.delete(0, END)
                phone_entry.insert(0, user_data[3])  # Phone Number
                
                email_entry.delete(0, END)
                email_entry.insert(0, user_data[4])  # Email
            else:
                messagebox.showerror("Not Found", "User not found.")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            conn.close()

    Label(user_window, text="Enter Patient ID", font=("Arial", 14), fg="#f06d95").place(x=50, y=120)
    patient_id = Entry(user_window, width=25, font=("Arial", 14), borderwidth=2, relief="solid")
    patient_id.place(x=50, y=150)

    fetch_btn = Button(user_window, text="Fetch User Data", width=20, font=("Arial", 14), bg="#57a1f8", fg="white", command=fetch_user_data)
    fetch_btn.place(x=350, y=150)

    Label(user_window, text="Name", font=("Arial", 14), fg="#f06d95").place(x=50, y=200)
    name_entry = Entry(user_window, width=25, font=("Arial", 14))
    name_entry.place(x=50, y=230)
    
    Label(user_window, text="Phone Number", font=("Arial", 14), fg="#f06d95").place(x=50, y=270)
    phone_entry = Entry(user_window, width=25, font=("Arial", 14))
    phone_entry.place(x=50, y=300)
    
    Label(user_window, text="Email", font=("Arial", 14), fg="#f06d95").place(x=50, y=340)
    email_entry = Entry(user_window, width=25, font=("Arial", 14))
    email_entry.place(x=50, y=370)

    #Update User Data
    def update_user():
        user_id = patient_id.get().strip()
        new_name = name_entry.get().strip()
        new_phone = phone_entry.get().strip()
        new_email = email_entry.get().strip()

        if not user_id.isdigit():
            messagebox.showerror("Invalid ID", "Please enter a valid patient ID.")
            return

        if not all([new_name, new_phone, new_email]):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
        
        try:
            conn = sqlite3.connect("signup.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE patient SET name=?, phone_number=?, email=? WHERE patient_id=?",
                           (new_name, new_phone, new_email, user_id))
            conn.commit()
            messagebox.showinfo("Success", "User details updated successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
        finally:
            conn.close()

    # Update Button
    update_btn = Button(user_window, text="Update User", width=20, font=("Arial", 14), bg="#57a1f8", fg="white", command=update_user)
    update_btn.place(x=50, y=420)

    #Delete User Data
    def delete_user():
        user_id = patient_id.get().strip()

        if not user_id.isdigit():
            messagebox.showerror("Invalid ID", "Please enter a valid patient ID.")
            return
        
        confirm = messagebox.askquestion("Delete User", "Are you sure you want to delete this user?")
        if confirm == 'yes':
            try:
                conn = sqlite3.connect("signup.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM patient WHERE patient_id=?", (user_id,))
                conn.commit()
                messagebox.showinfo("Success", "User deleted successfully.")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")
            finally:
                conn.close()

    # Delete Button
    delete_btn = Button(user_window, text="Delete User", width=20, font=("Arial", 14), bg="#ff6666", fg="white", command=delete_user)
    delete_btn.place(x=250, y=420)

    user_window.mainloop()

