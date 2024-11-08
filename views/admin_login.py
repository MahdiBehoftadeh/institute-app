import tkinter as tk

class AdminLoginPage:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        self.label_username = tk.Label(self.frame, text="Admin Username:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self.frame)
        self.entry_username.pack()

        self.label_password = tk.Label(self.frame, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.pack()

        self.button_login = tk.Button(self.frame, text="Login", command=self.login)
        self.button_login.pack(pady=10)

    def login(self):
        # Leave this function empty for now
        pass