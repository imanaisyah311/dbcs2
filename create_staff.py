import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime
import re

class CreateStaffPage(tk.Tk):
    def __init__(self, logged_in_username=None, user_role=None):
        super().__init__()

        self.title("Create Staff")
        self.geometry("400x400")  # Set the window size

        self.logged_in_username = logged_in_username
        self.user_role = user_role

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Create Staff", font=("Helvetica", 20))
        title_label.pack(pady=20)

        # Staff Information Section
        staff_info_frame = ttk.LabelFrame(self, text="Staff Information")
        staff_info_frame.pack(padx=20, pady=10, fill="both")

        tk.Label(staff_info_frame, text="Staff Name:").grid(row=0, column=0, sticky="w")
        self.staff_name_entry = tk.Entry(staff_info_frame)
        self.staff_name_entry.grid(row=0, column=1)

        tk.Label(staff_info_frame, text="Staff Email:").grid(row=1, column=0, sticky="w")
        self.staff_email_entry = tk.Entry(staff_info_frame)
        self.staff_email_entry.grid(row=1, column=1)

        tk.Label(staff_info_frame, text="Staff Role:").grid(row=2, column=0, sticky="w")
        self.staff_role_var = tk.StringVar()
        staff_roles = ["Sales", "HR", "Stock", "Sys Admin"]
        self.staff_role_dropdown = ttk.Combobox(staff_info_frame, textvariable=self.staff_role_var, values=staff_roles)
        self.staff_role_dropdown.grid(row=2, column=1)

        tk.Label(staff_info_frame, text="Staff Password:").grid(row=3, column=0, sticky="w")
        self.staff_password_entry = tk.Entry(staff_info_frame, show="*")
        self.staff_password_entry.grid(row=3, column=1)

        tk.Label(staff_info_frame, text="Confirm Password:").grid(row=4, column=0, sticky="w")
        self.confirm_password_entry = tk.Entry(staff_info_frame, show="*")
        self.confirm_password_entry.grid(row=4, column=1)

        # Button to Submit Staff Creation
        submit_button = tk.Button(self, text="Create Staff", command=self.create_staff)
        submit_button.pack(pady=20)

        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()

    def create_staff(self):
        # Get values from the entry fields
        staff_name = self.staff_name_entry.get()
        staff_email = self.staff_email_entry.get()
        staff_role = self.staff_role_dropdown.get()
        staff_password = self.staff_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        self.error_label.config(text="")

        # Input validation
        if not (staff_name and staff_email and staff_role and staff_password and confirm_password):
            self.show_error("Please fill in all fields.")
            return

        if not self.validate_email(staff_email):
            self.show_error("Invalid email format.")
            return

        if not self.validate_password(staff_password):
            self.show_error("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.")
            return

        if staff_password != confirm_password:
            self.show_error("Passwords do not match.")
            return

        # Role-based permission checks
        if self.user_role == "HR" and staff_role == "Sys Admin":
            self.show_error("HR staff cannot create Sys Admin staff.")
            return

        # Get current timestamp as staff creation date
        staff_creation_date = datetime.now()

        try:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Staff (Name, Email, Role, Staff_Creation_Date, Staff_Registrar, Staff_Password) VALUES (%s, %s, %s, %s, %s, %s)",
                (staff_name, staff_email, staff_role, staff_creation_date, self.logged_in_username, staff_password)
            )
            conn.commit()

            if staff_role == "Sys Admin":
                # After inserting the staff member and if their role is "Sys Admin",
                # create a SQL Server login for them and add them to the SalesSystem database
                 self.create_sql_server_login(staff_name, staff_password, "SalesSystem")

            self.clear_fields()  # Clear input fields
            self.show_message("Staff created successfully.")
        except Exception as e:
            if conn:
                conn.rollback()  # Rollback in case of errors
            self.show_error(f"Error creating staff: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def create_sql_server_login(self, username, password, database_name):
        try:
            # Connect to the master database
            conn_master = mysql.connector.connect(
                host="DESKTOP-A91QDH7",
                port= 3306,                      # Replace with your MySQL host
                user="SalesSystem",       # Replace with your MySQL username
                password="Shawn25@",   # Replace with your MySQL password
                database="SalesSystem"
            )

            cursor_master = conn_master.cursor()

            # Create a SQL Server login for the new staff member
            create_login_sql = f"CREATE LOGIN [{username}] WITH PASSWORD = '{password}', DEFAULT_DATABASE = [master], CHECK_POLICY = OFF;"
            cursor_master.execute(create_login_sql)

            # Commit the transaction in the master database
            conn_master.commit()

            # Connect to the specified database
            conn_sales = mysql.connector.connect(
                host="DESKTOP-A91QDH7",
                port= 3306,                      
                user="SalesSystem",       
                password="Shawn25@",   
                database="SalesSystem"
            )
            cursor_sales = conn_sales.cursor()

            # Create a user in the specified database
            create_user_sql = f"USE {database_name}; CREATE USER [{username}] FOR LOGIN [{username}];"
            cursor_sales.execute(create_user_sql)

            # Commit the transaction in the specified database
            conn_sales.commit()

            # Grant necessary permissions to the user in the specified database
            permissions = [
                "Members",
                "Staff",
                "Stock",
                "Orders"
            ]

            for obj in permissions:
                grant_permission_sql = f"USE {database_name}; GRANT SELECT ON {obj} TO [{username}];"
                cursor_sales.execute(grant_permission_sql)

            # Commit the transaction in the specified database
            conn_sales.commit()

            print(f"User '{username}' created and permissions granted successfully in database '{database_name}'.")
        except mysql.connector.Error as e:
            print("Error creating SQL Server login:", str(e))
        finally:
            if cursor_master:
                cursor_master.close()
            if cursor_sales:
                cursor_sales.close()
            if conn_master:
                conn_master.close()
            if conn_sales:
                conn_sales.close()


    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host="DESKTOP-A91QDH7",
                port= 3306,                      
                user="SalesSystem",       
                password="Shawn25@",   
                database="SalesSystem"
            )
            return conn
        except mysql.connector.Error as e:
            raise Exception(f"Database connection error: {e}")

    def clear_fields(self):
        self.staff_name_entry.delete(0, tk.END)
        self.staff_email_entry.delete(0, tk.END)
        self.staff_password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)

    def show_message(self, message):
        message_label = tk.Label(self, text=message)
        message_label.pack(pady=10)
        self.after(3000, message_label.destroy)  # Display the message for 3 seconds

    def show_error(self, message):
        self.error_label.config(text=message)

    def validate_email(self, email):
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_pattern, email) is not None

    def validate_password(self, password):
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
        return re.match(password_pattern, password) is not None

if __name__ == "__main__":
    app = CreateStaffPage()
    app.mainloop()
