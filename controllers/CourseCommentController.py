from helpers.AuthHelper import AuthHelper
from tabulate import tabulate

from models.Course import Course
from models.CourseComment import CourseComment
from models.UserCourse import UserCourse


class CourseCommentController:

    def __init__(self, connection):
        self.connection = connection
        self.course_comment_model = CourseComment(self.connection)

    def index(self):
        course_comments = self.course_comment_model.find_all()
        course_model = Course(self.connection)

        comments = []

        for course_comment in course_comments:
            course = course_model.find_one({'id': course_comment['course_id']})
            comments.append({
                'id': course_comment['id'],
                'comment': course_comment['comment'],
                'course_name': course['name'],
                'course_instructor': course['instructor'],
                'course_scheduled_day': course['scheduled_day'],
                'course_start_time': course['start_time'],
                'course_end_time': course['end_time'],
                'created_at': course_comment['created_at'],
            })

        self.__print_course_comment_table(comments)

    def create(self):
        auth_helper = AuthHelper()
        user = auth_helper.get_user(self.connection)

        user_course_model = UserCourse(self.connection)
        user_courses = user_course_model.find_all({
            'user_id': user['id']
        })

        course_model = Course(self.connection)

        courses = []

        for user_course in user_courses:
            course = course_model.find_one({
                'id': user_course['course_id'],
            })
            courses.append(course)

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

    def __print_course_comment_table(self, datas):
        table_data = [
            [
                data['id'],
                data['comment'],
                data['course_name'],
                data['course_instructor'],
                data['course_scheduled_day'],
                str(data['course_start_time']),
                str(data['course_end_time']),
                str(data['created_at']),
            ]
            for data in datas
        ]
        headers = [
            "ID", "Comment text", "Course Name", "Instructor", "Scheduled Day", "Start Time", "End Time",
            "Comment Created At"
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
