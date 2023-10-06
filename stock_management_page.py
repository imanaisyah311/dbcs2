import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime

class StockManagementHomePage(tk.Toplevel):
    def __init__(self, logged_in_user_id, logged_in_username, user_role):  # Add logged_in_user_id parameter
        super().__init__()

        self.title("Stock Management Home Page")
        self.geometry("1000x600")

        self.logged_in_user_id = logged_in_user_id
        self.logged_in_username = logged_in_username
        self.user_role = user_role

        self.conn = self.connect_db()  # Create a database connection
        self.cursor = self.conn.cursor()  # Create a cursor

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
        title_label = tk.Label(self, text="Stock Management", font=("Helvetica", 20))
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

        update_stock_frame = ttk.LabelFrame(self, text="Update Stock")
        update_stock_frame.pack(padx=20, pady=10, fill="both")

        self.update_item_var = tk.StringVar()
        items = ["Strawberry", "Banana", "Watermelon"]  # List of items, replace with actual items
        update_item_label = tk.Label(update_stock_frame, text="Select Item:")
        update_item_label.pack()

        update_item_dropdown = ttk.Combobox(update_stock_frame, textvariable=self.update_item_var, values=items)
        update_item_dropdown.pack()

        update_quantity_label = tk.Label(update_stock_frame, text="Quantity:")
        update_quantity_label.pack()

        self.update_quantity_entry = tk.Entry(update_stock_frame)
        self.update_quantity_entry.pack()

        update_button = tk.Button(update_stock_frame, text="Update", command=self.update_stock)
        update_button.pack(pady=10)

        # Delete Stock Section
        delete_stock_frame = ttk.LabelFrame(self, text="Delete Stock")
        delete_stock_frame.pack(padx=20, pady=10, fill="both")

        self.delete_item_var = tk.StringVar()
        delete_item_label = tk.Label(delete_stock_frame, text="Select Item:")
        delete_item_label.pack()

        delete_item_dropdown = ttk.Combobox(delete_stock_frame, textvariable=self.delete_item_var, values=items)
        delete_item_dropdown.pack()

        delete_quantity_label = tk.Label(delete_stock_frame, text="Quantity:")  # Add quantity label
        delete_quantity_label.pack()

        self.delete_quantity_entry = tk.Entry(delete_stock_frame)  # Quantity entry field
        self.delete_quantity_entry.pack()

        delete_button = tk.Button(delete_stock_frame, text="Delete", command=self.delete_stock)
        delete_button.pack(pady=10)

        # View Stock Section
        view_stock_button = tk.Button(self, text="View Stock", command=self.view_stock)
        view_stock_button.pack(pady=10)

        self.stock_treeview = ttk.Treeview(self, columns=("Item Name", "Price", "Count", "Last Restock Date"))
        self.stock_treeview.heading("Item Name", text="Item Name")
        self.stock_treeview.heading("Price", text="Price")
        self.stock_treeview.heading("Count", text="Count")
        self.stock_treeview.heading("Last Restock Date", text="Last Restock Date")

        self.stock_treeview.pack(fill="both", expand=True)

    def update_stock(self):
        item = self.update_item_var.get()
        quantity = int(self.update_quantity_entry.get())

        get_item_id_query = "SELECT ID FROM Stock WHERE Name = %s"
        self.cursor.execute(get_item_id_query, (item,))
        item_id_row = self.cursor.fetchone()

        if item_id_row:

            # Update stock quantity, last_restock_date, and StockerID
            update_query = f"UPDATE Stock SET Item_Count = Item_Count + %s, Last_Restock_Date = %s, Stocker_ID = %s WHERE Name = %s"
            restock_date = datetime.now().strftime('%Y-%m-%d')
            update_values = (quantity, restock_date, self.logged_in_user_id, item)

            self.cursor.execute(update_query, update_values)
            self.conn.commit()

            print(f"Added stock for {item}: Quantity = {quantity}")
        else:
            print(f"Item '{item}' not found in the database.")


    def delete_stock(self):
        item = self.delete_item_var.get()
        quantity = int(self.delete_quantity_entry.get())

        # Retrieve the item_id for the given item name
        get_item_id_query = "SELECT ID FROM Stock WHERE Name = %s"
        self.cursor.execute(get_item_id_query, (item,))
        item_id_row = self.cursor.fetchone()

        if item_id_row:

            # Update stock quantity, last_restock_date, and StockerID
            update_query = f"UPDATE Stock SET Item_Count = Item_Count - %s, Last_Restock_Date = %s, Stocker_ID = %s WHERE Name = %s"
            restock_date = datetime.now().strftime('%Y-%m-%d')
            update_values = (quantity, restock_date, self.logged_in_user_id, item)

            self.cursor.execute(update_query, update_values)
            self.conn.commit()

            print(f"Deleted stock for {item}: Quantity = {quantity}")
        else:
            print(f"Item '{item}' not found in the database.")


    def view_stock(self):
        # Retrieve all stock information from the database
        select_query = "SELECT Name, Price, Item_Count, Last_Restock_Date FROM stock"
        self.cursor.execute(select_query)
        stock_data = self.cursor.fetchall()

        # Clear existing content in the Treeview
        for item in self.stock_treeview.get_children():
            self.stock_treeview.delete(item)

        # Configure Treeview columns if not already configured
        if not self.stock_treeview['columns']:
            self.stock_treeview["columns"] = ("Name", "Item Price", "Item Count", "Last Restock Date")
            self.stock_treeview.heading("Name", text="Name")
            self.stock_treeview.heading("Item Price", text="Item Price")
            self.stock_treeview.heading("Item Count", text="Item Count")
            self.stock_treeview.heading("Last Restock Date", text="Last Restock Date")

        for item_name, item_price, item_count, last_restock_date in stock_data:
            self.stock_treeview.insert("", "end", values=(item_name, item_price, item_count, last_restock_date))

if __name__ == "__main__":
    
    app = StockManagementHomePage()
    app.mainloop()