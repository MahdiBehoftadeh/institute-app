import tkinter as tk

from configs.DatabaseConnection import DatabaseConnection
from helpers.AuthHelper import AuthHelper
from models.UserCourses import UserCourses


class MyCourses(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        db = DatabaseConnection()
        connection = db.connect()

        auth_helper = AuthHelper()
        user = auth_helper.get_user(connection)

        user_courses_model = UserCourses(connection)
        courses = user_courses_model.find_all({
            'user_id': user['id']
        })

        for course in courses:
            label = tk.Label(self, text=course['name'], font=("Helvetica", 16))
            label.pack(padx=10, pady=10)
