import json
import os

from helpers.EncryptionHelper import EncryptionHelper
from models.User import User


class AuthHelper:
    def __init__(self):
        self.storage_file = './storage/auth_data.txt'
        self.username = None
        self.user_type = None
        self.encryption_helper = EncryptionHelper()
        self.load_user_data()

    def load_user_data(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'rb') as file:
                    encrypted_data = file.read()
                    decrypted_data = self.encryption_helper.decrypt(encrypted_data)
                    data = json.loads(decrypted_data)  # Still use JSON for internal structure
                    self.username = data.get('username')
                    self.user_type = data.get('user_type')
            except Exception as e:
                print(f"Failed to load user data: {e}")
                if os.path.exists(self.storage_file):
                    os.remove(self.storage_file)

    def save_user_data(self):
        data = json.dumps({'username': self.username, 'user_type': self.user_type})
        encrypted_data = self.encryption_helper.encrypt(data)
        os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'wb') as file:
                file.write(encrypted_data)

    def login(self, username, user_type):
        self.username = username
        self.user_type = user_type
        self.save_user_data()

    def logout(self):
        self.username = None
        self.user_type = None
        if os.path.exists(self.storage_file):
            os.remove(self.storage_file)
        print("User logged out.")
        exit()


    def check(self):
        self.load_user_data()
        return self.username is not None

    def get_username(self):
        return self.username

    def get_type(self):
        return self.user_type

    def get_user(self, db_connection):
        user_model = User(db_connection)
        user = user_model.find_one({
            'username': self.username
        })
        return user