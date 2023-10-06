import tkinter as tk
from tkinter import ttk
import mysql.connector
import re

class MemberRegistrationPage(tk.Tk):
    def __init__(self, logged_in_user_id):
        super().__init__()

        self.title("Member Registration")
        self.geometry("600x600")  # Set the window size

        self.logged_in_user_id = logged_in_user_id

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Member Registration", font=("Helvetica", 20))
        title_label.pack(pady=20)

        # Personal Information Section
        personal_info_frame = ttk.LabelFrame(self, text="Personal Information")
        personal_info_frame.pack(padx=20, pady=10, fill="both")

        tk.Label(personal_info_frame, text="Full Name:").grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(personal_info_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(personal_info_frame, text="Email:").grid(row=1, column=0, sticky="w")
        self.email_entry = tk.Entry(personal_info_frame)
        self.email_entry.grid(row=1, column=1)

        tk.Label(personal_info_frame, text="Age:").grid(row=2, column=0, sticky="w")
        self.age_entry = tk.Entry(personal_info_frame)
        self.age_entry.grid(row=2, column=1)

        tk.Label(personal_info_frame, text="Home Address:").grid(row=3, column=0, sticky="w")
        self.address_entry = tk.Entry(personal_info_frame)
        self.address_entry.grid(row=3, column=1)

        tk.Label(personal_info_frame, text="Phone Number:").grid(row=4, column=0, sticky="w")
        self.phone_entry = tk.Entry(personal_info_frame)
        self.phone_entry.grid(row=4, column=1)

        tk.Label(personal_info_frame, text="Bank Card Number:").grid(row=5, column=0, sticky="w")
        self.bank_card_entry = tk.Entry(personal_info_frame)
        self.bank_card_entry.grid(row=5, column=1)

        tk.Label(personal_info_frame, text="ID Card Number:").grid(row=6, column=0, sticky="w")
        self.id_card_entry = tk.Entry(personal_info_frame)
        self.id_card_entry.grid(row=6, column=1)

        tk.Label(personal_info_frame, text="Postcode:").grid(row=7, column=0, sticky="w")
        self.postcode_entry = tk.Entry(personal_info_frame)
        self.postcode_entry.grid(row=7, column=1)

        tk.Label(personal_info_frame, text="State:").grid(row=8, column=0, sticky="w")
        self.state_entry = tk.Entry(personal_info_frame)
        self.state_entry.grid(row=8, column=1)

        tk.Label(personal_info_frame, text="Country:").grid(row=9, column=0, sticky="w")
        self.country_entry = tk.Entry(personal_info_frame)
        self.country_entry.grid(row=9, column=1)

        # Button to Submit Registration
        submit_button = tk.Button(self, text="Submit", command=self.submit_registration)
        submit_button.pack(pady=20)

    def submit_registration(self):
        # Use self.logged_in_user_id to access the currently logged-in user's ID
        # This ID can be used for database operations or other purposes

        # Get values from the entry fields
        name = self.name_entry.get()
        email = self.email_entry.get()
        age = self.age_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        bank_card = self.bank_card_entry.get()
        id_card = self.id_card_entry.get()
        postcode = self.postcode_entry.get()
        state = self.state_entry.get()
        country = self.country_entry.get()

        # Input validation
        if not (name and email and age and address and phone and bank_card and id_card and postcode and state and country):
            print("Please fill in all fields.")
            return

        if not self.validate_email(email):
            print("Invalid email format.")
            return

        if not self.validate_phone(phone):
            print("Invalid phone number format. Please use the format 0161111111.")
            return

        if not self.validate_bank_card(bank_card):
            print("Invalid bank card number format. Please use a 8-digit number.")
            return

        if not self.validate_id_card(id_card):
            print("Invalid ID card number format. Please use the format 123456789012.")
            return

        if not self.validate_postcode(postcode):
            print("Invalid postcode format. Please use a 5 to 6 digit number.")
            return
        
        if not self.validate_age(age):
            print("Invalid age format or age out of range (18-99).")
            return
        
        try:
            self.insert_member_data(name, email, age, address, phone, bank_card, id_card, postcode, state, country)
            self.show_info("Registration successful!")
        except Exception as e:
            self.show_error(f"Error: {e}")

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

    def insert_member_data(self, name, email, age, address, phone, bank_card, id_card, postcode, state, country):
        try:
            conn = self.connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO Members (Name, Email, Age, Address, Phone, Bank_Card, ID_Card, Postcode, State, Country, RegistrantID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (name, email, age, address, phone, bank_card, id_card, postcode, state, country, self.logged_in_user_id)
            )

            conn.commit()
            conn.close()
        except mysql.connector.Error as e:
            raise Exception(f"Database insert error: {e}")

    def validate_email(self, email):
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(email_pattern, email) is not None

    def validate_bank_card(self, bank_card):
        # Validate bank card number: 8 digits
        bank_card_pattern = r"^\d{8}$" 
        return re.match(bank_card_pattern, bank_card) is not None

    def validate_postcode(self, postcode):
        # Validate postcode: 5 digits
        postcode_pattern = r"^\d{5}$"
        return re.match(postcode_pattern, postcode) is not None

    def validate_id_card(self, id_card):
        # Validate ID card number: 12
        id_card_pattern = r"^\d{12}$" 
        return re.match(id_card_pattern, id_card) is not None

    def validate_phone(self, phone):
        # Validate 10-digit phone number
        phone_pattern = r"^\d{10}$" 
        return re.match(phone_pattern, phone) is not None
    
    def validate_age(self, age):
        try:
            age = int(age)
            if age < 18 or age > 99:
                return False
            return True
        except ValueError:
            return False
    
    def show_error(self, message):
        error_label = ttk.Label(self, text=message, foreground="red")
        error_label.pack()

    def show_info(self, message):
        info_label = ttk.Label(self, text=message, foreground="green")
        info_label.pack()

if __name__ == "__main__":

    app = MemberRegistrationPage()
    app.mainloop()
    