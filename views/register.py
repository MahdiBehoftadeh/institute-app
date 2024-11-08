import tkinter as tk
from tkinter import messagebox
from configs.DatabaseConnection import DatabaseConnection
from controllers.UserController import UserController

class RegisterPage:
    def __init__(self, root, go_to_login_callback):
        self.root = root
        self.go_to_login_callback = go_to_login_callback

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        self.label_name = tk.Label(self.frame, text="Name:")
        self.label_name.pack()
        self.entry_name = tk.Entry(self.frame)
        self.entry_name.pack()

        self.label_username = tk.Label(self.frame, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.pack()

        self.label_password = tk.Label(self.frame, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.pack()

        self.button_register = tk.Button(self.frame, text="Register", command=self.register)
        self.button_register.pack(pady=10)

        # "Back to Login" button
        self.button_back = tk.Button(self.frame, text="Back to Login", command=self.go_to_login)
        self.button_back.pack()

    def register(self):
        # Create a connection to the database
        database = DatabaseConnection()
        connection = database.connect()

        # Retrieve the input from the entry widgets
        name = self.entry_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Instantiate the UserController and attempt to register the user
        user_controller = UserController(connection)
        is_successfully_registered = user_controller.register(name, username, password)

        if is_successfully_registered:
            # If registration is successful, navigate back to the login page
            self.frame.destroy()
            self.go_to_login_callback()
        else:
            # Show an error dialog if registration failed
            messagebox.showerror("Registration Failed", "Please try again.")

    def go_to_login(self):
        self.frame.destroy()
        self.go_to_login_callback()