import tkinter as tk
from tkinter import ttk
import mysql.connector

class MemberManagementPage(tk.Tk):
    def __init__(self, logged_in_user_id, logged_in_username, user_role):
        super().__init__()

        self.title("Member Management")
        self.geometry("1200x600")

        # Store user information
        self.logged_in_user_id = logged_in_user_id
        self.logged_in_username = logged_in_username
        self.user_role = user_role

        self.create_widgets()

    def create_widgets(self):
        # Create a table to display member data
        self.member_table = ttk.Treeview(self, columns=("ID", "Name", "Email", "Phone", "DeletedBy"), show="headings")
        self.member_table.heading("ID", text="ID")
        self.member_table.heading("Name", text="Name")
        self.member_table.heading("Email", text="Email")
        self.member_table.heading("Phone", text="Phone")
        self.member_table.heading("DeletedBy", text="Deleted by")  # Change to "DeletedBy" here
        self.member_table.pack(padx=20, pady=10, fill="both", expand=True)

        # Add a "View All Members" button
        view_button = tk.Button(self, text="View All Members", command=self.load_members)
        view_button.pack(pady=10)

        # Add a "Delete" button
        delete_button = tk.Button(self, text="Delete Member", command=self.delete_member)
        delete_button.pack(pady=10)

    def load_members(self):
        # Connect to your database (adjust the connection parameters as needed)
        conn = mysql.connector.connect(
            host="DESKTOP-A91QDH7",
            port= 3306,                      
            user="SalesSystem",       
            password="Shawn25@",   
            database="SalesSystem"
        )
        cursor = conn.cursor()

        # Fetch member data from the database (adjust the SQL query as needed)
        cursor.execute("""
            SELECT M.ID, M.Name, M.Email, M.Phone, S.Name AS DeletedByName
            FROM Members AS M
            LEFT JOIN Staff AS S ON M.DeletedBy = S.ID
        """)
        members = cursor.fetchall()

        # Clear the table
        for item in self.member_table.get_children():
            self.member_table.delete(item)

        # Populate the table with cleaned member data
        for member in members:
            cleaned_member = [str(item).replace(",", "").replace("'", "") if item is not None else "" for item in member]
            self.member_table.insert("", "end", values=cleaned_member)

        conn.close()

    def delete_member(self):
        selected_item = self.member_table.selection()
        if not selected_item:
            return

        member_id = self.member_table.item(selected_item, "values")[0]

        # Connect to your database (adjust the connection parameters as needed)
        conn = mysql.connector.connect(
            host="DESKTOP-A91QDH7",
            port= 3306,                      
            user="SalesSystem",       
            password="Shawn25@",   
            database="SalesSystem"
        )
        cursor = conn.cursor()

        try:
            # Update the DeletedBy column with the user's ID
            cursor.execute("UPDATE Members SET DeletedBy = %s WHERE ID = %s", (self.logged_in_user_id, member_id))

            conn.commit()
        except mysql.connector.Error as e:
            # Handle the database connection or query error here
            print("Database error:", e)
        finally:
            conn.close()

        # Refresh the member table
        self.load_members()

if __name__ == "__main__":

    app = MemberManagementPage()
    app.mainloop()
