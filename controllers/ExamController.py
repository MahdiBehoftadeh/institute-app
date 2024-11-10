from tabulate import tabulate

from helpers.AuthHelper import AuthHelper
from models.Exam import Exam
from models.Question import Question
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

    def user_start_exam(self):
        auth_helper = AuthHelper()
        user = auth_helper.get_user(self.connection)

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

        question_model = Question(self.connection)
        questions = question_model.find_all({
            'exam_id': exam_id
        })

        answers = []

        for question in questions:
            print(f"{question['text']} ({question['points']} points)")
            print(f"a. {question['option_a']}")
            print(f"b. {question['option_b']}")
            print(f"c. {question['option_c']}")
            print(f"d. {question['option_d']}")
            answer = input("\nEnter your choice(a/b/c/d): ")
            while answer not in ["a", "b", "c", "d"]:
                print(f"Invalid choice. Please choose from 'a', 'b', 'c', 'd'")
                answer = input("\nEnter your choice(a/b/c/d): ")
            answers.append({
                'question_id': question['id'],
                'question_text': question['text'],
                'chosen_answer': answer,
                'correct_answer': question['correct_answer'],
                'points': question['points'],
                'answered_correctly': bool(question['correct_answer'] == answer),
                'earned_points': int(question['correct_answer'] == answer) * question['points']
            })

        total_score = 0
        for answer in answers:
            total_score += answer['earned_points']

        user_exam_model = UserExam(self.connection)
        created_user_exam = user_exam_model.create({
            'user_id': user['id'],
            'exam_id': exam_id,
            'score': total_score
        })

        print(f"Exam {exam['name']} results: ")
        print(f"Total score: {total_score}")

        self.__print_started_exam_results_table(answers)

        if created_user_exam:
            print(f"Exam {exam['name']} saved successfully.")
        else:
            print("Failed to save exam.")



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

    def __print_started_exam_results_table(self, datas):
        table_data = [
            [
                data['question_id'],
                data['question_text'],
                data['chosen_answer'],
                data['correct_answer'],
                (str('Correct ✅') if data['correct_answer'] else str('Incorrect ❌')),
                data['earned_points'],
                data['points']
            ]
            for data in datas
        ]
        headers = ["Question ID", "Question", "Chosen Answer", "Correct Answer", "Answer Status", "Earned Points", "Question Points"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
