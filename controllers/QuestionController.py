from tabulate import tabulate

from controllers.ExamController import ExamController
from models.Exam import Exam
from models.Question import Question


class QuestionController:

    def __init__(self, connection):
        self.connection = connection
        self.exam_model = Question(self.connection)

    def create(self):

        exam_controller = ExamController(self.connection)
        exam_controller.index()

        exam_model = Exam(self.connection)
        exams = exam_model.find_all()

        exam_ids = [exam['id'] for exam in exams]

        exam_id = int(input("\nEnter exam ID: "))
        while exam_id not in exam_ids:
            print(f"Course {exam_id} does not exist")
            exam_id = int(input("\nEnter exam ID: "))

        text = input("\nEnter question text: ")
        correct_answer = input("\nEnter correct answer(a/b/c/d): ")
        option_a = input("\nEnter option A text: ")
        option_b = input("\nEnter option B text: ")
        option_c = input("\nEnter option C text: ")
        option_d = input("\nEnter option D text: ")
        points = input("\nEnter question points: ")

        created_question = self.exam_model.create({
            'exam_id': exam_id,
            'text': text,
            'correct_answer': correct_answer,
            'option_a': option_a,
            'option_b': option_b,
            'option_c': option_c,
            'option_d': option_d,
            'points': points,
        })

        if created_question:
            print(f"Question created successfully")
        else:
            print("Failed to create question")

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
        headers = ["ID", "Name", "Description", "Duration(s)", "Total Points", "Start At", "Expires At", "Created At",
                   "Updated At"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
