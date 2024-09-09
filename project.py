import customtkinter as ctk
from pymongo import MongoClient
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Connect to MongoDB
try:
    client = MongoClient('localhost', 27017)  # Replace with your MongoDB server details
    db = client['PY']
    collection = db['users']
    orders_collection = db['buy']
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    input("Press Enter to exit...")
    exit()

# Set appearance mode
ctk.set_appearance_mode("dark")

# Create the main application window
root = ctk.CTk()
root.geometry("500x400")
root.title("KK COMERSE BD")

def soft():
    products = ["IPHONE 14 Pro Max", "Samsung Galaxy S8+", "SYMPHONY  12"]

    def show_login_frame():
        frame_register.pack_forget()
        frame_login.pack(pady=10, padx=20, fill="both", expand=True)

    def show_product_frame():
        frame_login.pack_forget()
        frame_product.pack(pady=10, padx=20, fill="both", expand=True)

    def register():
        name = entry_name.get()
        email = entry_email.get()
        password = entry_password.get()
        user = {"name": name, "email": email, "password": password}
        try:
            result = collection.insert_one(user)
            print(f"Inserted user with id: {result.inserted_id}")
            label_result.configure(text="Registration successful! Please log in.")
            entry_name.delete(0, 'end')
            entry_email.delete(0, 'end')
            entry_password.delete(0, 'end')
            show_login_frame()
        except Exception as e:
            print(f"Error inserting user: {e}")
            label_result.configure(text=f"Registration failed: {e}")

    def login():
        name = entry_login_name.get()
        email = entry_login_email.get()
        password = entry_login_password.get()
        user = collection.find_one({"name": name, "email": email, "password": password})
        if user:
            print(f"User {name} logged in successfully.")
            label_login_result.configure(text=f"Hello {name}, you are logged in!")
            show_product_frame()
        else:
            print("Login failed.")
            label_login_result.configure(text="Login failed. Please try again.")

    def buy_product():
        product_choice = product_var.get()
        name = entry_login_name.get()
        order = {"name": name, "product": product_choice}
        try:
            result = orders_collection.insert_one(order)
            print(f"Inserted order with id: {result.inserted_id}")
            label_product_result.configure(text=f"{name}, you bought {product_choice}!")
        except Exception as e:
            print(f"Error inserting order: {e}")
            label_product_result.configure(text=f"Purchase failed: {e}")

    # Create and place widgets for registration
    frame_register = ctk.CTkFrame(master=root)
    frame_register.pack(pady=10, padx=20, fill="both", expand=True)

    label_name = ctk.CTkLabel(master=frame_register, text="Enter your name:")
    label_name.pack(pady=5)
    entry_name = ctk.CTkEntry(master=frame_register)
    entry_name.pack(pady=5)

    label_email = ctk.CTkLabel(master=frame_register, text="Enter your email:")
    label_email.pack(pady=5)
    entry_email = ctk.CTkEntry(master=frame_register)
    entry_email.pack(pady=5)

    label_password = ctk.CTkLabel(master=frame_register, text="Enter your password:")
    label_password.pack(pady=5)
    entry_password = ctk.CTkEntry(master=frame_register, show="*")
    entry_password.pack(pady=5)

    button_register = ctk.CTkButton(master=frame_register, text="Register", command=register)
    button_register.pack(pady=10)

    label_result = ctk.CTkLabel(master=frame_register, text="")
    label_result.pack(pady=5)

    # Create and place widgets for login
    frame_login = ctk.CTkFrame(master=root)

    label_login_name = ctk.CTkLabel(master=frame_login, text="Enter your name:")
    label_login_name.pack(pady=5)
    entry_login_name = ctk.CTkEntry(master=frame_login)
    entry_login_name.pack(pady=5)

    label_login_email = ctk.CTkLabel(master=frame_login, text="Enter your email:")
    label_login_email.pack(pady=5)
    entry_login_email = ctk.CTkEntry(master=frame_login)
    entry_login_email.pack(pady=5)

    label_login_password = ctk.CTkLabel(master=frame_login, text="Enter your password:")
    label_login_password.pack(pady=5)
    entry_login_password = ctk.CTkEntry(master=frame_login, show="*")
    entry_login_password.pack(pady=5)

    button_login = ctk.CTkButton(master=frame_login, text="Login", command=login)
    button_login.pack(pady=10)

    label_login_result = ctk.CTkLabel(master=frame_login, text="")
    label_login_result.pack(pady=5)

    # Create and place widgets for product selection and buying
    frame_product = ctk.CTkFrame(master=root)

    product_var = ctk.StringVar(value=products[0])
    dropdown = ctk.CTkOptionMenu(master=frame_product, variable=product_var, values=products)
    dropdown.pack(pady=5)

    button_buy = ctk.CTkButton(master=frame_product, text="Buy", command=buy_product)
    button_buy.pack(pady=10)

    label_product_result = ctk.CTkLabel(master=frame_product, text="")
    label_product_result.pack(pady=5)

# Call the function to set up the GUI
soft()

# Start the main loop
root.mainloop()

# Pause to keep the console window open
input("Press Enter to exit...")
