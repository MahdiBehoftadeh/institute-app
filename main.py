import os
import tkinter as tk

from dotenv import load_dotenv

from helpers.AuthHelper import AuthHelper
from views.user_login import UserLoginPage
from views.register import RegisterPage
from views.admin_dashboard import AdminDashboardPage
from views.user_dashboard import UserDashboardPage


def show_user_login_page(root):
    UserLoginPage(root, lambda: show_user_dashboard_page(root))

def show_register_page(root):
    RegisterPage(root, lambda: show_user_dashboard_page(root))

def show_user_dashboard_page(root):
    UserDashboardPage(root)

def show_admin_dashboard_page(root):
    AdminDashboardPage(root)

if __name__ == "__main__":
    load_dotenv()

    root = tk.Tk()

    width = 1300
    height = 700

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.title(os.getenv('APP_NAME'))

    auth_helper = AuthHelper()
    if auth_helper.check():
        if auth_helper.get_type() == 'user':
            show_user_dashboard_page(root)
        elif auth_helper.get_type() == 'admin':
            show_admin_dashboard_page(root)
        else:
            show_user_login_page(root)
    else:
        show_user_login_page(root)
    root.mainloop()