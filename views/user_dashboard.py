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

class RegisterCourse(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        db = DatabaseConnection()
        self.connection = db.connect()

        course_model = Course(self.connection)
        courses = course_model.find_all()

        self.main_frame = tk.Frame(parent)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_frame, height=500, width=400)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.cards_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")

        self.create_cards(courses)

        self.cards_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def create_cards(self, courses):
        for course in courses:
            days = {
                'saturday': 'شنبه',
                'sunday': 'یکشنبه',
                'monday': 'دوشنبه',
                'tuesday': 'سه شنبه',
                'wednesday': 'چهارشنبه',
                'thursday': 'پنجشنبه',
            }

            scheduled_day = days.get(course['scheduled_day'].lower(), 'Unknown')

            card_frame = tk.Frame(self.cards_frame, relief="solid", borderwidth=1)
            card_frame.pack(pady=5, padx=5, fill="x")

            label_name = tk.Label(card_frame, text="نام کلاس: "+course['name'])
            label_name.pack(anchor="w")

            label_instructor = tk.Label(card_frame, text="نام استاد: "+course['instructor'])
            label_instructor.pack(anchor="w")

            label_schedule = tk.Label(card_frame, text="روز و ساعت: "+scheduled_day+" ها از ساعت "+str(course['start_time'])+" تا "+str(course['end_time']))
            label_schedule.pack(anchor="w")

            label_location = tk.Label(card_frame, text="محل برگزاری: "+course['location'])
            label_location.pack(anchor="w")

            # Pass the course ID to the register method using lambda
            button = tk.Button(card_frame, text="ثبت نام", command=lambda c_id=course['id']: self.register(c_id))
            button.pack(anchor="e")

    def register(self, course_id):
        auth_helper = AuthHelper()
        user = auth_helper.get_user(self.connection)
        user_courses_model = UserCourses(self.connection)
        user_courses_model.create({
            'user_id': user['id'],
            'course_id': course_id
        })
        print(f"User registered in class successfully.")


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")


class UserDashboardPage:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Sidebar frame
        self.sidebar = tk.Frame(self.frame, width=300)
        self.sidebar.pack(side="left", fill="y")

        # Sidebar buttons
        sidebar_buttons = ["کلاس های من", "ثبت نام کلاس جدید", "VIP منابع", "آزمون آنلاین", "حساب کاربری", "خروج"]
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
        # Remove the current page if it exists
        if self.current_page:
            self.current_page.pack_forget()
            self.current_page.destroy()  # Fully destroy the widget
            self.current_page = None

        # Load the new page
        if page_name == "کلاس های من":
            self.current_page = MyCourses(self.content_frame)
        elif page_name == "ثبت نام کلاس جدید":
            self.current_page = RegisterCourse(self.content_frame)
        else:
            self.current_page = tk.Label(self.content_frame, text=f"Page: {page_name} content", font=("Helvetica", 16))

        # Pack the current page
        self.current_page.pack(fill="both", expand=True)