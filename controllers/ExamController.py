from tabulate import tabulate

from models.Exam import Exam
from models.User import User
from models.UserExam import UserExam


class ExamController:

    def __init__(self, connection):
        self.connection = connection
        self.exam_model = Exam(self.connection)

    def index(self):
        exams = self.exam_model.find_all()
        self.__print_exams_table(exams)

    def create(self):
        name = input('Enter exam name: ')
        description = input('Enter exam description: ')
        duration = input('Enter exam duration: ')
        total_points = input('Enter exam total points: ')
        start_time = input('Enter exam start time: ')
        end_time = input('Enter exam end time: ')

        created_exam = self.exam_model.create({
            'name': name,
            'description': description,
            'duration': duration,
            'total_points': total_points,
            'starts_at': start_time,
            'expires_at': end_time
        })

        if created_exam:
            print(f'Exam {name} created successfully.')
        else:
            print('Failed to create exam.')

    def user_exams_index(self):
        self.index()

        exams = self.exam_model.find_all()

        exam_ids = [exam['id'] for exam in exams]

        exam_id = int(input("\nEnter exam ID: "))
        while exam_id not in exam_ids:
            print(f"Course {exam_id} does not exist")
            exam_id = int(input("\nEnter exam ID: "))

        exam = self.exam_model.find_one({
            'id': exam_id
        })

        user_exam_model = UserExam(self.connection)
        user_exams = user_exam_model.find_all({
            'exam_id': exam_id
        })

        results = []

        for user_exam in user_exams:
            user_model = User(self.connection)
            user = user_model.find_one({
                'id': user_exam['user_id']
            })

            results.append({
                'id': user_exam['id'],
                'user_name': user['name'],
                'user_username': user['username'],
                'score': f"{user_exam['score']} / {exam['total_points']}",
                'exam_start_time': exam['starts_at'],
                'exam_end_time': exam['expires_at'],
                'completed_at': user_exam['completed_at']
            })

        print(f"Exam {exam['name']} results: ")
        self.__print_exam_results_table(results)



    def __print_exams_table(self, datas):
        table_data = [
            [
                data['id'],
                data['name'],
                data['description'],
                data['duration'],
                data['total_points'],
                str(data['starts_at']),
                str(data['expires_at']),
                str(data['created_at']),
                str(data['updated_at'])
            ]
            for data in datas
        ]
        headers = ["ID", "Name", "Description", "Duration(s)", "Total Points", "Start At", "Expires At", "Created At", "Updated At"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    def __print_exam_results_table(self, datas):
        table_data = [
            [
                data['id'],
                data['user_name'],
                data['user_username'],
                data['score'],
                str(data['exam_start_time']),
                str(data['exam_end_time']),
                str(data['completed_at'])
            ]
            for data in datas
        ]
        headers = ["ID", "User Name", "User Username", "Score", "Start Time", "Expiration Time", "Completion Time"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
