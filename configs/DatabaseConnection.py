import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


class DatabaseConnection:
    def __init__(self):
        load_dotenv()

        self.host = os.getenv("DATABASE_HOST")
        self.user = os.getenv("DATABASE_USERNAME")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.database = os.getenv("DATABASE_NAME")
        self.port = os.getenv("DATABASE_PORT")
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return self.connection
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

    def execute_sql_file(self, file_path):
        if not self.connection:
            print("No database connection established.")
            return

        try:
            with open(file_path, 'r') as file:
                sql_script = file.read()
            cursor = self.connection.cursor()
            cursor.execute(sql_script)
            self.connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error executing SQL file: {e}")
            self.connection.rollback()

    def migrate(self):
        self.execute_sql_file('../database/migrations.sql')
        print("Migration completed.")

    def seed(self):
        self.execute_sql_file('../database/seeder.sql')
        print("Seed completed.")

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()