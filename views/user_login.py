import tkinter as tk
from tkinter import messagebox

from configs.DatabaseConnection import DatabaseConnection
from controllers.UserController import UserController
from views.register import RegisterPage


class UserLoginPage:
    def __init__(self, root, go_to_register_callback):
        self.root = root
        self.go_to_register_callback = go_to_register_callback

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        self.label_username = tk.Label(self.frame, text="Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.pack()

        self.label_password = tk.Label(self.frame, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.pack()

        self.button_login = tk.Button(self.frame, text="Login", command=self.login)
        self.button_login.pack(pady=10)

        self.link_register = tk.Button(self.frame, text="Register", command=self.go_to_register)
        self.link_register.pack()

    def login(self):
        # Create a connection to the database
        database = DatabaseConnection()
        connection = database.connect()

        # Retrieve the input from the entry widgets
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Instantiate the UserController and attempt to register the user
        user_controller = UserController(connection)
        is_successfully_logged_in = user_controller.login(username, password)

        if is_successfully_logged_in:
            # If registration is successful, navigate back to the login page
            self.frame.destroy()
            self.go_to_register_callback()
        else:
            # Show an error dialog if registration failed
            messagebox.showerror("Login Failed", "Please try again.")


    def go_to_register(self):
        self.frame.destroy()
        RegisterPage(self.root, self.go_to_register_callback)
