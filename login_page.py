import tkinter as tk
from tkinter import messagebox
from system_admin import SystemAdminHomePage
from sales_page import SalesHomePage
from stock_management_page import StockManagementHomePage
from hr_page import HRHomePage
import mysql.connector

# Import other home page classes as needed

class LoginPage(tk.Tk):
    def __init__(self, main_app=None):
        super().__init__()

        self.title("Login Page")
        self.geometry("500x500")

        self.main_app = main_app  # Store reference to the MainApplication instance

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Login Page", font=("Helvetica", 20))
        title_label.pack(pady=20)

        user_type_frame = tk.Frame(self)
        user_type_frame.pack()

        user_type_label = tk.Label(user_type_frame, text="Select User Type:")
        user_type_label.pack(side="left")

        self.user_type = tk.StringVar()
        user_type_options = ["Sales", "Stock", "HR", "Sys Admin"]
        user_type_menu = tk.OptionMenu(user_type_frame, self.user_type, *user_type_options)
        user_type_menu.pack(side="left")

        username_label = tk.Label(self, text="Username:")
        username_label.pack(pady=10)

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        self.username_entry.insert(0, "Shawn")

        password_label = tk.Label(self, text="Password:")
        password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        self.password_entry.insert(0, "Shawn2525")

        login_button = tk.Button(self, text="Login", command=self.login)
        login_button.pack(pady=20)

    def connect_db(self):
        conn = mysql.connector.connect(
            host="DESKTOP-A91QDH7",
            port= 3306,                      # Replace with your MySQL host
            user="SalesSystem",       # Replace with your MySQL username
            password="Shawn25@",   # Replace with your MySQL password
            database="SalesSystem"     # Replace with your MySQL database name   
        )
        return conn   

    def open_home_page(self, logged_in_user_id, logged_in_username, logged_in_role):
        if logged_in_role == "Sales":
            app = SalesHomePage(logged_in_user_id, logged_in_username, logged_in_role)
        elif logged_in_role == "Stock":
            app = StockManagementHomePage(logged_in_user_id, logged_in_username, logged_in_role)
        elif logged_in_role == "HR":
            app = HRHomePage(logged_in_user_id, logged_in_username, logged_in_role)
        elif logged_in_role == "Sys Admin":
            app = SystemAdminHomePage(logged_in_user_id, logged_in_username, logged_in_role)
        
        app.protocol("WM_DELETE_WINDOW", self.on_home_page_close)  # Handle home page close event
        self.withdraw()  # Hide the login page
        app.mainloop()

    def on_home_page_close(self):
        self.destroy()  # Destroy the home page window

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        selected_user_type = self.user_type.get()

        user_info = self.get_user_info(username, password, selected_user_type)

        if user_info:
            logged_in_user_id, logged_in_username, logged_in_role = user_info  # Unpack the user_info tuple
            self.open_home_page(logged_in_user_id, logged_in_username, logged_in_role)
        else:
            messagebox.showerror("Invalid Login", "Invalid username, password, or user type.")

    def get_user_info(self, username, password, selected_user_type):
        conn = mysql.connector.connect(
            host="DESKTOP-A91QDH7",
            port= 3306,                      # Replace with your MySQL host
            user="SalesSystem",       # Replace with your MySQL username
            password="Shawn25@",   # Replace with your MySQL password
            database="SalesSystem"   
        )

        cursor = conn.cursor()

        # Query the database to validate the username and password and retrieve user information
        query = "SELECT ID, Name, Role FROM Staff WHERE Name = %s AND Staff_Password = %s AND Role = %s"
        cursor.execute(query, (username, password, selected_user_type))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user

if __name__ == "__main__":
    login_app = LoginPage()
    login_app.mainloop()
