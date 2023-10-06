import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime
from member_registration import MemberRegistrationPage

class SalesHomePage(tk.Toplevel):
    def __init__(self, logged_in_user_id, logged_in_username, user_role):
        super().__init__()

        self.title("Sales Application")
        self.geometry("1000x600")

        self.logged_in_user_id = logged_in_user_id
        self.logged_in_username = logged_in_username
        self.user_role = user_role

        self.item_prices = {
            "Banana": 6.00,
            "Watermelon": 8.00,
            "Strawberry": 5.00
        }

        self.selected_item = tk.StringVar()
        self.quantity = tk.StringVar()

        self.items_in_table = {}

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
        
         # Display User Information
        user_info_frame = tk.Frame(self)
        user_info_frame.pack()

        user_id_label = tk.Label(user_info_frame, text=f"User ID: {self.logged_in_user_id}")
        user_id_label.pack(side="left")

        username_label = tk.Label(user_info_frame, text=f"Username: {self.logged_in_username}")
        username_label.pack(side="left")

        role_label = tk.Label(user_info_frame, text=f"Role: {self.user_role}")
        role_label.pack(side="left")

        # Item Selection
        item_label = ttk.Label(self, text="Select Item:")
        item_label.pack()

        item_dropdown = ttk.Combobox(self, textvariable=self.selected_item, values=list(self.item_prices.keys()))
        item_dropdown.pack()

        quantity_label = ttk.Label(self, text="Quantity:")
        quantity_label.pack()

        quantity_entry = ttk.Entry(self, textvariable=self.quantity)
        quantity_entry.pack()

        add_button = ttk.Button(self, text="Add Item", command=self.add_item)
        add_button.pack()

        # Item Table
        self.item_table = ttk.Treeview(self, columns=("Item", "Quantity", "Price", "Total Price"), show="headings")
        self.item_table.heading("Item", text="Item")
        self.item_table.heading("Quantity", text="Quantity")
        self.item_table.heading("Price", text="Price (RM)")
        self.item_table.heading("Total Price", text="Total Price (RM)")
        self.item_table.pack()

        # Total Price
        self.total_price = 0.0
        self.total_label = ttk.Label(self, text=f"Total Price: {self.total_price:.2f} RM")
        self.total_label.pack()

        # Delete Button
        delete_button = ttk.Button(self, text="Delete Selected Item", command=self.delete_selected_item)
        delete_button.pack()

        submit_button = ttk.Button(self, text="Submit", command=self.submit_sale)  # Added Submit button
        submit_button.pack()

        register_member_button = ttk.Button(self, text="Register Member", command=self.create_and_open_member_registration)
        register_member_button.pack()

    def add_item(self):
        item = self.selected_item.get()
        quantity = self.quantity.get()

        if item and quantity.isdigit():
            quantity = int(quantity)
            if quantity > 0:
                price = self.item_prices.get(item, 0)
                total_item_price = price * quantity

                # Check if the item already exists in the table
                if item in self.items_in_table:
                    # Update the quantity and total price
                    existing_quantity, existing_total_price = self.items_in_table[item]
                    new_quantity = existing_quantity + quantity
                    new_total_price = existing_total_price + total_item_price
                    self.items_in_table[item] = (new_quantity, new_total_price)

                    # Update the table
                    self.update_table()
                else:
                    # Add the item to the dictionary
                    self.items_in_table[item] = (quantity, total_item_price)

                    # Add the item to the table
                    self.item_table.insert("", "end", values=(item, quantity, f"{price:.2f}", f"{total_item_price:.2f}"))

                # Update total price
                self.total_price += total_item_price
                self.total_label.config(text=f"Total Price: {self.total_price:.2f} RM")

                # Clear input fields
                self.selected_item.set("")
                self.quantity.set("")
            else:
                self.show_error("Quantity must be a positive integer.")
        else:
            self.show_error("Please select an item and enter a valid quantity.")

    def update_table(self):
        # Clear the table
        for item in self.item_table.get_children():
            self.item_table.delete(item)

        # Update the table with the items from the dictionary
        for item, (quantity, total_price) in self.items_in_table.items():
            price = self.item_prices.get(item, 0)
            self.item_table.insert("", "end", values=(item, quantity, f"{price:.2f}", f"{total_price:.2f}"))

    def delete_selected_item(self):
        selected_item = self.item_table.selection()
        if selected_item:
            for item in selected_item:
                item_name = self.item_table.item(item, "values")[0]
                quantity, total_price = self.items_in_table[item_name]
                self.total_price -= total_price
                self.total_label.config(text=f"Total Price: {self.total_price:.2f} RM")
                self.item_table.delete(item)
                del self.items_in_table[item_name]
        else:
            self.show_error("Please select an item to delete.")

    def show_error(self, message):
        error_label = ttk.Label(self, text=message, foreground="red")
        error_label.pack()

    def submit_sale(self):
        # Get the current date and time
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Connect to the database
        conn = self.connect_db()
        cursor = conn.cursor()

        try:
            # Check if there is sufficient stock for each item in the sale
            for item_name, (quantity, _) in self.items_in_table.items():
                cursor.execute(
                    "SELECT Item_Count FROM Stock WHERE Name = %s",
                    (item_name,)
                )
                stock_result = cursor.fetchone()

                if stock_result is not None:
                    stock_quantity = stock_result[0]

                    if quantity > stock_quantity:
                        conn.rollback()
                        conn.close()
                        self.show_error(f"Not enough stock for {item_name}.")
                        return
                else:
                    conn.rollback()
                    conn.close()
                    self.show_error(f"Item {item_name} not found in the inventory.")
                    return

            # Insert sale data into the database
            cursor.execute(
                "INSERT INTO Orders (Total_Price, Date_of_Sale, CashierID) VALUES (%s, %s, %s)",
                (self.total_price, current_datetime, self.logged_in_user_id)
            )

            # Deduct sold quantities from the stock
            for item_name, (quantity, _) in self.items_in_table.items():
                cursor.execute(
                    "UPDATE Stock SET Item_Count = Item_Count - %s WHERE Name = %s",
                    (quantity, item_name)
                )

            # Commit the transaction
            conn.commit()
            conn.close()

            # Reset the table and total price
            self.items_in_table = {}
            self.update_table()
            self.total_price = 0.0
            self.total_label.config(text=f"Total Price: {self.total_price:.2f} RM")

        except Exception as e:
            # Handle any exceptions here (e.g., log the error)
            print(f"Error: {e}")

    def create_and_open_member_registration(self):
        member_registration_window = MemberRegistrationPage(self.logged_in_user_id)
        member_registration_window.mainloop()
            

if __name__ == "__main__":
    app = SalesHomePage()
    app.open_member_registration() 
    app.mainloop()
