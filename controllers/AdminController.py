from helpers.AuthHelper import AuthHelper
from helpers.HashHelper import HashHelper
from models.Admin import Admin


class AdminController:

    def __init__(self, db_connection):
        self.connection = db_connection

    def login(self, username, password):
        admin_model = Admin(self.connection)
        admin = admin_model.find_one({
            'username': username,
            'password': HashHelper.hash(password)
        })
        if admin:
            auth_helper = AuthHelper()
            auth_helper.login(admin['id'], 'admin')
            print('Admin logged in successfully.')
        else:
            print('Failed to authenticate admin, either username or password is incorrect.')

    def logout(self):
        auth_helper = AuthHelper()
        if not auth_helper.check():
            print('Admin was not logged in.')
            return False

        auth_helper.logout()
        print('Admin logged out.')
        return True
