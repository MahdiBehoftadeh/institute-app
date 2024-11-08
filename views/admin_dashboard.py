import tkinter as tk

class AdminDashboardPage:
    def __init__(self, root):
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        label_admin_welcome = tk.Label(self.frame, text="Welcome to the Admin Dashboard!")
        label_admin_welcome.pack()