import tkinter as tk

from configs.DatabaseConnection import DatabaseConnection
from helpers.AuthHelper import AuthHelper
from models.Course import Course
from models.UserCourses import UserCourses


class MyCourses(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Get the database connection
        db = DatabaseConnection()
        connection = db.connect()

        # Get user details
        auth_helper = AuthHelper()
        user = auth_helper.get_user(connection)

        # Get user courses
        user_courses_model = UserCourses(connection)
        courses = user_courses_model.find_all({
            'user_id': user['id']
        })

        # Display the courses
        for course in courses:
            course_model = Course(connection)
            course_details = course_model.find_one({'id': course['id']})
            #
            # # Create a frame for the card
            # card_frame = tk.Frame(self, bg="white", relief="", borderwidth=2, padx=10, pady=10)
            # card_frame.pack(padx=10, pady=10, fill="x", expand=True)
            #
            # # Title label
            # title_label = tk.Label(card_frame, text=course_details['name'], font=("Helvetica", 16, "bold"), bg="white", fg="black")
            # title_label.pack(pady=(0, 5))
            #
            # # Description label
            # description_label = tk.Label(card_frame, text=course_details['instructor'], wraplength=250, bg="white", fg="black")
            # description_label.pack()


class UserDashboardPage:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Sidebar frame
        self.sidebar = tk.Frame(self.frame, width=300)
        self.sidebar.pack(side="left", fill="y")

        # Sidebar buttons
        sidebar_buttons = ["My Courses", "Register Course", "VIP Resources", "Online Exams", "Profile", "Logout"]
        self.page_frames = {}  # Store the page frames

        # Buttons to switch between pages
        for btn_text in sidebar_buttons:
            button = tk.Button(self.sidebar, text=btn_text, command=lambda btn=btn_text: self.load_page(btn))
            button.pack(pady=5, fill="x")

        # Content area to display pages
        self.content_frame = tk.Frame(self.frame)
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Initial page (Empty or Home)
        self.current_page = None
        self.load_page("My Courses")  # Default page when the app starts

    def load_page(self, page_name):
        # Hide the current page if it exists
        if self.current_page:
            self.current_page.pack_forget()

        # Load the new page
        if page_name == "My Courses":
            self.current_page = MyCourses(self.content_frame)  # Assign to current_page
        else:
            self.current_page = tk.Label(self.content_frame, text=f"Page: {page_name} content", font=("Helvetica", 16))

        # Pack the current page
        self.current_page.pack(fill="both", expand=True)