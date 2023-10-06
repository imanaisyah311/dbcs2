import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime
import tkinter.messagebox as messagebox
from create_staff import CreateStaffPage

class RemoveStaff(tk.Toplevel):
    def __init__(self, logged_in_user_id, logged_in_username, user_role):
        super().__init__()

        self.title("Remove Staff")
        self.geometry("1000x600")  # Set the window size

        self.logged_in_user_id = logged_in_user_id
        self.logged_in_username = logged_in_username
        self.user_role = user_role

        self.create_widgets()

    def connect_db(self):
        conn = mysql.connector.connect(
            host="DESKTOP-A91QDH7",
            port= 3306,                      
            user="SalesSystem",       
            password="Shawn25@",   
            database="SalesSystem"    
        )
        return conn

    def create_widgets(self):
        title_label = tk.Label(self, text="Remove Staff", font=("Helvetica", 20))
        title_label.pack(pady=20)

        # Add HR-specific functionality here
        view_staff_button = tk.Button(self, text="View Staff", command=self.view_staff)
        view_staff_button.pack(pady=10)

        # Add "Delete Staff" button
        delete_staff_button = tk.Button(self, text="Delete Staff", command=self.delete_selected_staff)
        delete_staff_button.pack(pady=10)

        self.staff_table = ttk.Treeview(self, columns=("ID", "Name", "Email", "Staff Role", "Staff Status"), show="headings")        
        self.staff_table.heading("ID", text="ID")
        self.staff_table.heading("Name", text="Name")
        self.staff_table.heading("Email", text="Email")
        self.staff_table.heading("Staff Role", text="Staff Role")
        self.staff_table.heading("Staff Status", text="Staff Status")
        self.staff_table.pack()

    def delete_selected_staff(self):
        selected_item = self.staff_table.selection()
        if selected_item:
            # Get the selected staff member's ID
            staff_id = self.staff_table.item(selected_item[0], "values")[0]

            # Confirm termination with the user
            confirm_termination = messagebox.askyesno("Confirm Termination", "Are you sure you want to terminate this staff member%s")
            if confirm_termination:
                # Connect to your HR-related database or system
                conn = self.connect_db()
                cursor = conn.cursor()
       
                terminator_name =  self.logged_in_username 

                # Get the current date and time
                termination_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Update the selected staff member's status to 'Terminated' and record the terminator name and date
                update_query = "UPDATE Staff SET status = 'Terminated', TerminatedBy = %s, TerminationDate = %s WHERE ID = %s"
                cursor.execute(update_query, (terminator_name, termination_date, staff_id))
                conn.commit()
                conn.close()

        else:
            tk.messagebox.showinfo("No Selection", "Please select a staff member to terminate.")


    def view_staff(self):
        # Connect to your HR-related database or system
        conn = self.connect_db()
        cursor = conn.cursor()

        # Retrieve staff data (name, email, staff role) from your HR database
        query = "SELECT ID, Name, Email, Role, Status FROM Staff"  # Modify this query as per your database schema
        cursor.execute(query)
        staff_data = cursor.fetchall()

        # Clear the existing data in the table
        for row in self.staff_table.get_children():
            self.staff_table.delete(row)

        # Insert the retrieved data into the table without parentheses, commas, and apostrophes
        for row in staff_data:
            clean_row = [str(item) for item in row]  # Convert each item to a string
            self.staff_table.insert("", "end", values=clean_row)

        conn.close()

if __name__ == "__main__":

    app = RemoveStaff()
    app.mainloop()
