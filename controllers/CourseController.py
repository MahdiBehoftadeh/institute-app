from helpers.AuthHelper import AuthHelper
from models.Course import Course
from tabulate import tabulate

from models.CourseComment import CourseComment
from models.UserCourse import UserCourse


class CourseController:

    def __init__(self, connection):
        self.connection = connection
        self.course_model = Course(self.connection)

    def index(self):
        courses = self.course_model.find_all()
        self.__print_course_table(courses)

    def user_courses(self):
        auth_helper = AuthHelper()
        user = auth_helper.get_user(self.connection)

        user_course_model = UserCourse(self.connection)
        user_courses = user_course_model.find_all({
            'user_id': user['id']
        })

        courses = []

        for user_course in user_courses:
            course = self.course_model.find_one({
                'id': user_course['course_id'],
            })
            courses.append(course)

        self.__print_course_table(courses)

    def enroll_in_class(self):
        auth_helper = AuthHelper()
        user = auth_helper.get_user(self.connection)

        courses = self.course_model.find_all()
        self.__print_course_table(courses)
        course_ids = [course['id'] for course in courses]

        course_id = int(input("\nEnter Course ID: "))
        while course_id not in course_ids:
            print(f"Course {course_id} does not exist")
            course_id = int(input("\nEnter Course ID: "))

        user_courses_model = UserCourse(self.connection)

        already_enrolled = user_courses_model.find_one({
            'user_id': user['id'],
            'course_id': course_id
        })

        if already_enrolled:
            print(f"Course {course_id} already enrolled")
            return

        enrolled_in_class = user_courses_model.create({
            'user_id': user['id'],
            'course_id': course_id,
        })
        if enrolled_in_class:
            print(f"Enrolled course successfully")
        else:
            print(f"Failed to enroll in {course_id} class")

    def comment_on_class(self):
        auth_helper = AuthHelper()
        user = auth_helper.get_user(self.connection)

        user_course_model = UserCourse(self.connection)
        user_courses = user_course_model.find_all({
            'user_id': user['id']
        })

        courses = []

        for user_course in user_courses:
            course = self.course_model.find_one({
                'id': user_course['course_id'],
            })
            courses.append(course)

        if courses.__len__() < 1:
            print(f"User has not enrolled any courses")
            return None

        self.__print_course_table(courses)
        course_ids = [course['id'] for course in courses]

        course_id = int(input("\nEnter Course ID: "))
        while course_id not in course_ids:
            print(f"Course {course_id} does not exist")
            course_id = int(input("\nEnter Course ID: "))

        comment = input("\nEnter your comment: ")

        course_comment_model = CourseComment(self.connection)
        created_course_comment = course_comment_model.create({
            'course_id': course_id,
            'comment': comment,
        })

        if created_course_comment:
            print(f"Course comment successfully submitted")
        else:
            print(f"Failed to create course comment")

    def create(self):
        name = input("\nEnter course name: ")
        description = input("Enter course description: ")
        instructor = input("Enter instructor: ")
        max_students = input("Enter max students: ")
        location = input("Enter location: ")
        scheduled_day = input("Enter scheduled day(saturday/sunday/monday/tuesday/wednesday/thursday): ")
        start_time = input("Enter start time: ")
        end_time = input("Enter end time: ")
        start_date = input("Enter start date: ")
        end_date = input("Enter end date: ")
        enrollment_start_date = input("Enter enrollment start date: ")
        enrollment_end_date = input("Enter enrollment end date: ")

        created_course = self.course_model.create({
            'name': name,
            'description': description,
            'instructor': instructor,
            'max_students': max_students,
            'location': location,
            'scheduled_day': scheduled_day,
            'start_time': start_time,
            'end_time': end_time,
            'start_date': start_date,
            'end_date': end_date,
            'enrollment_start_date': enrollment_start_date,
            'enrollment_end_date': enrollment_end_date
        })

        if created_course:
            print(f"Course {name} successfully created")
        else:
            print(f"Failed to create course")

    def __print_course_table(self, courses):
        table_data = [
            [
                course['id'],
                course['name'],
                course['instructor'],
                course['location'],
                course['scheduled_day'],
                str(course['start_time']),
                str(course['end_time']),
            ]
            for course in courses
        ]
        headers = [
            "ID", "Course Name", "Instructor",
            "Location", "Scheduled Day", "Start Time", "End Time"
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
