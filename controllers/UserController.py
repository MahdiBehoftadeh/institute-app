from helpers.AuthHelper import AuthHelper
from helpers.HashHelper import HashHelper
from models.User import User


class UserController:

    def __init__(self, db_connection):
        self.connection = db_connection

    def login(self, username, password):
        user_model = User(self.connection)
        user = user_model.find_one({
            'username': username,
            'password': HashHelper.hash(password)
        })
        if user:
            auth_helper = AuthHelper()
            auth_helper.login(user['id'], 'user')
            print('User logged in successfully.')
            return True
        else:
            print('Failed to authenticate user, either username or password is incorrect.')
            return False

    def register(self, name, username, password):
        auth_helper = AuthHelper()
        if auth_helper.check():
            print('Already logged in.')
            return False

        user_model = User(self.connection)
        user = user_model.create({
            'name': name,
            'username': username,
            'password': HashHelper.hash(password),
        })
        if not user:
            print('Failed to register user.')
            return False

        auth_helper.login(username, 'user')
        print('User registered successfully.')
        return True

    def logout(self):
        auth_helper = AuthHelper()
        if not auth_helper.check():
            print('User was not logged in.')
            return False

        auth_helper.logout()
        print('User logged out.')
        return True

    

    # def request_vip(self):
    #     auth_helper = AuthHelper()
    #     if not auth_helper.check():
    #         print('Failed to authenticate user, either username or password is incorrect.')
    #         return False
    #
    #     user_model = User(self.connection)
    #     user_model.