import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from configs.DatabaseConnection import DatabaseConnection
from controllers.UserController import UserController
from helpers.AuthHelper import AuthHelper


# Placeholder page classes
class MyCourses(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Label for the page
        tk.Label(self, text="کلاس های من", font=("Arial", 16)).pack(pady=10)

        # Treeview (table) for courses
        self.tree = ttk.Treeview(self, columns=("Course", "Instructor", "Schedule", "Location"), show="headings")
        self.tree.heading("Course", text="نام کلاس")
        self.tree.heading("Instructor", text="استاد")
        self.tree.heading("Schedule", text="زمان‌بندی")
        self.tree.heading("Location", text="محل برگزاری")

        # Sample data for the table
        courses = [
            ("Python Programming", "Dr. Smith", "Monday 10:00 AM", "xxxx"),
            ("Data Science", "Prof. Lee", "Wednesday 2:00 PM", "xxxx"),
            ("Web Development", "Ms. Davis", "Friday 11:00 AM", "xxxx"),
        ]

        # Inserting data into the table
        for course in courses:
            self.tree.insert("", "end", values=course)

        # Pack the table
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")


class RegisterCourse(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Label for the page
        tk.Label(self, text="ثبت نام کلاس جدید", font=("Arial", 16)).pack(pady=10)

        # Treeview (table) for available classes
        self.tree = ttk.Treeview(self, columns=("Course", "Instructor", "Schedule", "Location", "Status"),
                                 show="headings")
        self.tree.heading("Course", text="نام کلاس")
        self.tree.heading("Instructor", text="استاد")
        self.tree.heading("Schedule", text="زمان‌بندی")
        self.tree.heading("Location", text="محل برگزاری")
        self.tree.heading("Status", text="وضعیت")

        # Sample data for available classes
        self.available_classes = [
            ("Python Programming", "Dr. Smith", "Monday 10:00 AM", "Room 101"),
            ("Data Science", "Prof. Lee", "Wednesday 2:00 PM", "Room 202"),
            ("Web Development", "Ms. Davis", "Friday 11:00 AM", "Room 303"),
        ]

        # Insert the available classes into the table
        for course in self.available_classes:
            self.tree.insert("", "end", values=course + ("ثبت نام",))  # Add "Register" to Status column

        # Pack the table
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Register button outside the table
        self.register_button = tk.Button(self, text="ثبت نام", state="disabled", command=self.register)
        self.register_button.pack(pady=10)

        # Bind tree selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def on_select(self, event):
        # Get selected row
        selected_item = self.tree.selection()
        if selected_item:
            # Check if the course is already registered
            course_status = self.tree.item(selected_item)["values"][4]  # Check the status column
            if course_status == "ثبت شده":
                # Disable the register button if already registered
                self.register_button.config(state="disabled", text="ثبت شده")
            else:
                # Enable the register button for the selected course
                self.register_button.config(state="normal", command=lambda: self.register(selected_item))

    def register(self, selected_item):
        # Handle the registration logic here
        course_name = self.tree.item(selected_item)["values"][0]

        # Registration process (you can add more logic here)
        print(f"Registering for {course_name}")

        # Update the row status to "ثبت شده" (Registered)
        self.tree.item(selected_item, values=list(self.tree.item(selected_item)["values"][:4]) + ["ثبت شده"])

        # Disable the register button and update its text
        self.register_button.config(state="disabled", text="ثبت شده")

        # Optionally show a confirmation message
        messagebox.showinfo("Registration", f"Successfully registered for {course_name}")


class VipResources(tk.Frame):
    def __init__(self, parent, show_details_callback):
        super().__init__(parent)
        self.show_details_callback = show_details_callback

        # Label for the page
        tk.Label(self, text="منابع VIP", font=("Arial", 16)).pack(pady=10)

        # Treeview (table) for VIP resources
        self.tree = ttk.Treeview(self, columns=("Resource", "Description", "View Details"), show="headings")
        self.tree.heading("Resource", text="منبع")
        self.tree.heading("Description", text="توضیحات")
        self.tree.heading("View Details", text="مشاهده جزئیات")

        # Sample data for VIP resources (Table of Contents)
        self.vip_resources = [
            ("Python Programming Book", "A comprehensive guide to Python."),
            ("Data Science Course", "An advanced course in data science."),
            ("Web Development Tutorial", "Learn full-stack web development."),
        ]

        # Insert the resources into the table
        for resource in self.vip_resources:
            self.tree.insert("", "end", values=(resource[0], resource[1], "View"))

        # Pack the table
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Bind tree selection event
        self.tree.bind("<ButtonRelease-1>", self.on_select)

    def on_select(self, event):
        # Get selected row
        selected_item = self.tree.selection()
        if selected_item:
            # Get the resource name and description
            resource_name = self.tree.item(selected_item)["values"][0]
            description = self.tree.item(selected_item)["values"][1]

            # Use the callback to show the detailed resource page
            self.show_details_callback(resource_name, description)


class ResourceDetailPage(tk.Frame):
    def __init__(self, parent, resource_name, resource_description):
        super().__init__(parent)
        self.resource_name = resource_name
        self.resource_description = resource_description

        # Display the resource details
        tk.Label(self, text="Resource Details", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Resource: " + self.resource_name, font=("Arial", 14)).pack(pady=5)
        tk.Label(self, text="Description: " + self.resource_description, font=("Arial", 12)).pack(pady=5)


class OnlineExam(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="آزمون آنلاین").pack()


class ProfilePage(tk.Frame):
    def __init__(self, parent, show_details_callback=None):
        super().__init__(parent)

        self.show_details_callback = show_details_callback

        # Simulated user data
        self.username = "johndoe"
        self.name = "John Doe"
        self.password = "password123"
        self.vip_request_status = "requested"  # This can be "requested", "accepted", or "rejected"

        # Title
        title = tk.Label(self, text="Profile Page", font=("Arial", 24))
        title.pack(pady=20)

        # Name Entry
        self.name_var = tk.StringVar(value=self.name)
        name_label = tk.Label(self, text="Name:")
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(self, textvariable=self.name_var)
        self.name_entry.pack(pady=5)

        # Username Entry
        self.username_var = tk.StringVar(value=self.username)
        username_label = tk.Label(self, text="Username:")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self, textvariable=self.username_var)
        self.username_entry.pack(pady=5)

        # Password Entry
        self.password_var = tk.StringVar(value=self.password)
        password_label = tk.Label(self, text="Password:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*", textvariable=self.password_var)
        self.password_entry.pack(pady=5)

        # Update Profile Button
        update_button = tk.Button(self, text="Update Profile", command=self.update_profile)
        update_button.pack(pady=10)

        # VIP Request Status
        self.vip_status_label = tk.Label(self, text=f"VIP Request Status: {self.vip_request_status.capitalize()}", font=("Arial", 16))
        self.vip_status_label.pack(pady=10)

        # VIP Request Button
        self.vip_button = tk.Button(self, text="Request VIP", command=self.request_vip)
        self.vip_button.pack(pady=10)

        # Hide the VIP request button based on the current status
        self.update_vip_button_visibility()

        # Change color based on VIP request status
        self.update_status_color()

    def update_profile(self):
        """ Update the profile with the entered details """
        self.name = self.name_var.get()
        self.username = self.username_var.get()
        self.password = self.password_var.get()

        # Here you can update the backend or database as needed
        print(f"Updated Profile: Name={self.name}, Username={self.username}, Password={self.password}")

        # Show a message to confirm the profile was updated
        confirmation_label = tk.Label(self, text="Profile Updated!", fg="green")
        confirmation_label.pack(pady=5)

    def update_status_color(self):
        """ Update the status label color based on the VIP request status. """
        if self.vip_request_status == "requested":
            self.vip_status_label.config(fg="yellow")
        elif self.vip_request_status == "accepted":
            self.vip_status_label.config(fg="green")
        elif self.vip_request_status == "rejected":
            self.vip_status_label.config(fg="red")

    def update_vip_button_visibility(self):
        """ Hide the VIP request button if the user has already requested or been accepted. """
        if self.vip_request_status in ["requested", "accepted"]:
            self.vip_button.pack_forget()  # Hide the button
        else:
            self.vip_button.pack(pady=10)  # Show the button if not requested or accepted

    def request_vip(self):
        """ Simulate the user making a VIP request or changing their status. """
        if self.vip_request_status == "requested":
            self.vip_request_status = "accepted"  # Change the status to accepted
        elif self.vip_request_status == "accepted":
            self.vip_request_status = "rejected"  # Change the status to rejected
        else:
            self.vip_request_status = "requested"  # Change the status to requested

        self.vip_status_label.config(text=f"VIP Request Status: {self.vip_request_status.capitalize()}")
        self.update_status_color()
        self.update_vip_button_visibility()  # Update button visibility after the status change


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Title
        tk.Label(self, text="ورود", font=("Arial", 24)).pack(pady=20)

        # Username Entry
        tk.Label(self, text="نام کاربری:").pack(pady=5)  # "Username:"
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        # Password Entry
        tk.Label(self, text="کلمه عبور:").pack(pady=5)  # "Password:"
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        login_button = tk.Button(self, text="ورود", command=self.login)  # "Login"
        login_button.pack(pady=20)

        # Register Link

        tk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterPage")).pack()


    def login(self):
        """ Simulate the login process and transition to the profile page """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Placeholder validation logic
        if username == "johndoe" and password == "password123":
            print("ورود موفقیت آمیز بود.")  # "Login successful"
            self.on_login_success()  # Call the callback to transition to the next page
        else:
            print("نام کاربری یا کلمه عبور اشتباه است.")  # "Invalid username or password"
            messagebox.showerror("Login Error", "نام کاربری یا کلمه عبور اشتباه است.")  # Error message


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Title
        tk.Label(self, text="ثبت نام", font=("Arial", 24)).pack(pady=20)  # "Register"

        tk.Label(self, text="نام:").pack(pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        # Username Entry
        tk.Label(self, text="نام کاربری:").pack(pady=5)  # "Username:"
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        # Password Entry
        tk.Label(self, text="کلمه عبور:").pack(pady=5)  # "Password:"
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        # Register Button
        register_button = tk.Button(self, text="ثبت نام", command=self.register)  # "Register"
        register_button.pack(pady=20)


    def register(self):
        """ Simulate the registration process """
        name = self.name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        print(f"Registered with: Username={username}, Password={password}, Email={username}")
        messagebox.showinfo("Registration Successful", "ثبت نام با موفقیت انجام شد.")  # Success message




# Main application class
class InstituteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Institute App")
        self.geometry("1000x600")

        self.auth_helper = AuthHelper()
        self.auth_helper.check()

        # Frame for sidebar
        if self.auth_helper.check():
            sidebar = tk.Frame(self, width=200, bg="gray")
            sidebar.pack(side="left", fill="y")

        # Main frame for page content
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(side="right", expand=True, fill="both")

        # if not self.auth_helper.check():
        #     self.login_page.pack()
        #     return

        # Buttons for sidebar navigation
        buttons = [
            ("کلاس های من", MyCourses),
            ("ثبت نام کلاس جدید", RegisterCourse),
            ("منابع VIP", VipResources),
            ("آزمون آنلاین", OnlineExam),
            ("حساب کاربری", ProfilePage),  # Profile page
            ("خروج", self.logout)
        ]

        self.frames = {}
        for F in (LoginPage, RegisterPage, MyCourses):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame

        for text, page_class in buttons[:-1]:  # Exclude the logout button for now
            button = tk.Button(sidebar, text=text, command=lambda cls=page_class: self.show_frame(cls))
            button.pack(fill="x", padx=5, pady=5)

        # Logout button
        logout_button = tk.Button(sidebar, text="خروج", command=self.logout)
        logout_button.pack(fill="x", padx=5, pady=5)

        # Display the login page initially
        self.show_frame(MyCourses)

    def on_login_success(self):
        self.show_frame(MyCourses)

    def show_frame_auth(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def show_frame(self, page_class, *args):
        # Remove existing frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Add show_details_callback argument to pages that need it
        if page_class == VipResources:
            page = page_class(self.main_frame, show_details_callback=self.show_details_callback)
        elif page_class == ProfilePage:
            page = page_class(self.main_frame, show_details_callback=self.show_details_callback)  # Pass to ProfilePage if needed
        elif page_class == ResourceDetailPage:
            page = page_class(self.main_frame, *args)  # Pass arguments (resource details)
        else:
            page = page_class(self.main_frame)

        page.pack(expand=True, fill="both")

    def show_details_callback(self, resource_name, resource_description):
        # To show details on resource pages
        self.show_frame(ResourceDetailPage, resource_name, resource_description)

    def logout(self):
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:
            self.auth_helper.logout()
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)


# Run the app
if __name__ == "__main__":
    app = InstituteApp()
    app.mainloop()
