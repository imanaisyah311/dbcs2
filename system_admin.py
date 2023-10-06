import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime
import tkinter.messagebox as messagebox
from create_staff import CreateStaffPage
from member_registration import MemberRegistrationPage
from manage_stock import ManageStock
from remove_staff import RemoveStaff
from member_management import MemberManagementPage

class SystemAdminHomePage(tk.Toplevel):
    def __init__(self, logged_in_user_id, logged_in_username, user_role):
        super().__init__()

        self.title("System Admin Home Page")
        self.geometry("800x800")

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
        title_label = tk.Label(self, text="System Admin Home Page", font=("Helvetica", 20))
        title_label.pack(pady=20)

        # Display User Information
        user_info_frame = tk.Frame(self)
        user_info_frame.pack()

        user_id_label = tk.Label(user_info_frame, text=f"User ID: {self.logged_in_user_id}")
        user_id_label.pack(side="left")

        username_label = tk.Label(user_info_frame, text=f"Username: {self.logged_in_username}")
        username_label.pack(side="left")

        role_label = tk.Label(user_info_frame, text=f"Role: {self.user_role}")
        role_label.pack(side="left")

        # Centered buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        register_member_button = tk.Button(button_frame, text="Register Member", command=self.create_and_open_member_registration)
        member_management_button = tk.Button(button_frame, text="View & Manage Members", command=self.create_and_open_view_members)
        add_staff_button = tk.Button(button_frame, text="Add Staff", command=self.create_and_open_create_staff)
        delete_staff_button = tk.Button(self, text="Delete Staff", command=self.create_and_open_remove_staff)
        manage_stock_button = tk.Button(button_frame, text="Manage Stock", command=self.create_and_open_manage_stock)
        
        register_member_button.pack(pady=10)
        member_management_button.pack(pady=10)
        add_staff_button.pack(pady=10)
        delete_staff_button.pack(pady=10)
        manage_stock_button.pack(pady=10)
        
        
        # Total Sales Section
        total_sales_frame = ttk.LabelFrame(self, text="Total Sales")
        total_sales_frame.pack(padx=20, pady=10, fill="both")

        start_date_label = tk.Label(total_sales_frame, text="Start Date:")
        start_date_label.pack()

        # Use DateEntry from tkcalendar for selecting start date
        self.start_date_entry = DateEntry(total_sales_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_date_entry.pack()

        end_date_label = tk.Label(total_sales_frame, text="End Date:")
        end_date_label.pack()

        # Use DateEntry from tkcalendar for selecting end date
        self.end_date_entry = DateEntry(total_sales_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_date_entry.pack()

        calculate_total_sales_button = tk.Button(self, text="Calculate Total Sales", command=self.calculate_total_sales_button_click)
        calculate_total_sales_button.pack(pady=10)

        self.total_sales_label = tk.Label(total_sales_frame, text="")
        self.total_sales_label.pack()
    
    def calculate_total_sales_button_click(self):
        start_date = self.start_date_entry.get_date().strftime('%Y-%m-%d')
        end_date = self.end_date_entry.get_date().strftime('%Y-%m-%d')
        total_sales = self.calculate_total_sales(start_date, end_date)
        self.total_sales_label.config(text=f"Total Sales from {start_date} to {end_date}: ${total_sales:.2f}")

    def calculate_total_sales(self, start_date, end_date):
        try:
            # Convert start_date and end_date strings to datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Connect to the SQL Server database (use your database connection details)
            conn = mysql.connector.connect(
                host="DESKTOP-A91QDH7",
                port= 3306,                      
                user="SalesSystem",       
                password="Shawn25@",   
                database="SalesSystem"
            )
            cursor = conn.cursor()

            # Construct and execute the SQL query to calculate total sales
            query = """
                SELECT SUM(Total_Price) 
                FROM Orders 
                WHERE Date_of_Sale BETWEEN %s AND %s
            """
            cursor.execute(query, (start_date, end_date))

            # Fetch the result
            total_sales = cursor.fetchone()[0]

            # Close the database connection
            conn.close()

            return total_sales
        except Exception as e:
            print(f"Error calculating total sales: {str(e)}")
            return 0  # Return 0 in case of an error

    def create_and_open_member_registration(self):
        member_registration_window = MemberRegistrationPage(self.logged_in_user_id)
        member_registration_window.mainloop()

    def create_and_open_remove_staff(self):
        remove_staff_window = RemoveStaff(self.logged_in_user_id, self.logged_in_username, self.user_role)
        remove_staff_window.mainloop()

    def create_and_open_create_staff(self):
        staff_registration_window = CreateStaffPage(self.logged_in_username,self.user_role)
        staff_registration_window.mainloop()

    def create_and_open_manage_stock(self):
        manage_stock_window = ManageStock(self.logged_in_user_id, self.logged_in_username, self.user_role)
        manage_stock_window.mainloop()

    def create_and_open_view_members(self):
        manage_members_window = MemberManagementPage(self.logged_in_user_id, self.logged_in_username, self.user_role)
        manage_members_window.mainloop()

if __name__ == "__main__":
    app = SystemAdminHomePage() 
    app.mainloop()
