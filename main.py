from configs.DatabaseConnection import DatabaseConnection
from controllers.CourseCommentController import CourseCommentController
from controllers.CourseController import CourseController
from controllers.ExamController import ExamController
from controllers.QuestionController import QuestionController
from controllers.UserController import UserController
from controllers.VipResourceController import VipResourceController
from helpers.AuthHelper import AuthHelper
from controllers.AdminController import AdminController


class Main:
    def __init__(self, connection):
        self.connection = connection
        print("""
        ██╗███╗   ██╗███████╗████████╗██╗████████╗██╗   ██╗████████╗███████╗     █████╗ ██████╗ ██████╗ 
        ██║████╗  ██║██╔════╝╚══██╔══╝██║╚══██╔══╝██║   ██║╚══██╔══╝██╔════╝    ██╔══██╗██╔══██╗██╔══██╗
        ██║██╔██╗ ██║███████╗   ██║   ██║   ██║   ██║   ██║   ██║   █████╗      ███████║██████╔╝██████╔╝
        ██║██║╚██╗██║╚════██║   ██║   ██║   ██║   ██║   ██║   ██║   ██╔══╝      ██╔══██║██╔═══╝ ██╔═══╝ 
        ██║██║ ╚████║███████║   ██║   ██║   ██║   ╚██████╔╝   ██║   ███████╗    ██║  ██║██║     ██║     
        ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝   ╚═╝    ╚═════╝    ╚═╝   ╚══════╝    ╚═╝  ╚═╝╚═╝     ╚═╝     
        """)

    def show_user_menus(self):
        menus = {
            1: "List of my classes",
            2: "Enroll in class",
            3: "Comment on a course",
            4: "VIP Resources",
            5: "Request VIP Account",
            6: "Edit Profile",
            7: "Start online exam",
            8: "Logout",
        }

        print("\nLogged in as user\n")
        for key, value in menus.items():
            print(f"{key}. {value}")

    def show_admin_menus(self):
        menus = {
            1: "List of all classes",
            2: "Create new class",
            3: "See course comments",
            4: "List of VIP Requests",
            5: "Answer VIP Requests",
            6: "List of all VIP resources",
            7: "Create new VIP resource",
            8: "List of all users",
            9: "List of all exams",
            10: "Create new exam",
            11: "Create question for exam",
            12: "List of all exams results",
            13: "Logout",
        }

        print("\nLogged in as admin\n")
        for key, value in menus.items():
            print(f"{key}. {value}")

    def handle_user_choice(self, choice):
        auth_helper = AuthHelper()
        course_controller = CourseController(self.connection)
        user_controller = UserController(self.connection)
        exam_controller = ExamController(self.connection)

        if choice == '1':
            course_controller.user_courses()
        elif choice == '2':
            course_controller.enroll_in_class()
        elif choice == '3':
            course_controller.comment_on_class()
        elif choice == '4':
            if auth_helper.get_user(self.connection)['vip'] == 'accepted':
                vip_resource_controller = VipResourceController(self.connection)
                vip_resource_controller.index()
            else:
                print("You are not a VIP user and can not access the VIP resources")
        elif choice == '5':
            user_controller.request_vip_account()
        elif choice == '6':
            user_controller.edit_profile()
        elif choice == '7':
            exam_controller.user_start_exam()
        elif choice == '8':
            auth_helper.logout()
        else:
            print("Invalid choice. Please try again.")

    def handle_admin_choice(self, choice):
        auth_helper = AuthHelper()
        course_controller = CourseController(self.connection)
        user_controller = UserController(self.connection)
        course_comment_controller = CourseCommentController(self.connection)
        vip_resource_controller = VipResourceController(self.connection)
        exam_controller = ExamController(self.connection)
        question_controller = QuestionController(self.connection)

        if choice == '1':
            course_controller.index()
        elif choice == '2':
            course_controller.create()
        elif choice == '3':
            course_comment_controller.index()
        elif choice == '4':
            user_controller.vip_requests_index()
        elif choice == '5':
            user_controller.vip_requests_answer()
        elif choice == '6':
            vip_resource_controller.index()
        elif choice == '7':
            vip_resource_controller.create()
        elif choice == '8':
            user_controller.index()
        elif choice == '9':
            exam_controller.index()
        elif choice == '10':
            exam_controller.create()
        elif choice == '11':
            question_controller.create()
        elif choice == '12':
            exam_controller.user_exams_index()
        elif choice == '13':
            auth_helper.logout()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":

    database = DatabaseConnection()
    connection = database.connect()

    app = Main(connection)

    auth_helper = AuthHelper()
    while not auth_helper.check():
        user_type = input("\nSelect account type (admin/user): ")
        if user_type == "admin":
            username = input("Enter username: ")
            password = input("Enter password: ")
            admin_controller = AdminController(connection)
            admin_controller.login(username, password)
        elif user_type == "user":
            auth_type = input("\nDo you want to login or register (login/register): ")
            user_controller = UserController(connection)
            if auth_type == "login":
                username = input("Enter username: ")
                password = input("Enter password: ")
                user_controller.login(username, password)
            elif auth_type == "register":
                name = input("Enter name: ")
                username = input("Enter username: ")
                password = input("Enter password: ")
                user_controller.register(name, username, password)
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Invalid choice. Please try again.")

    while True:
        if auth_helper.get_type() == 'user':
            app.show_user_menus()
            choice = input("\nEnter your choice: ")
            app.handle_user_choice(choice)
        elif auth_helper.get_type() == 'admin':
            app.show_admin_menus()
            choice = input("\nEnter your choice: ")
            app.handle_admin_choice(choice)
        else:
            print("Fatal error. Restart the program.")
