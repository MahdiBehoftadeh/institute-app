from tabulate import tabulate

from helpers.AuthHelper import AuthHelper
from helpers.HashHelper import HashHelper
from models.User import User


class UserController:

    def __init__(self, connection):
        self.connection = connection
        self.user_model = User(self.connection)


    def login(self, username, password):
        print(HashHelper.hash(password))
        user = self.user_model.find_one({
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

        user = self.user_model.create({
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

    def request_vip_account(self):
        choice = input('Would you like to request vip account? (y/n): ')
        if choice == 'n':
            return False

        auth_helper = AuthHelper()
        user = auth_helper.get_user(self.connection)

        if user['vip'] == 'requested' or user['vip'] == 'accepted':
            print('User already requested.')
            return False

        requested = self.user_model.update({
            'id': user['id']
        },{
            'vip': 'requested'
        })
        if requested:
            print('VIP request sent successfully.')
            return True
        else:
            print('Failed to send VIP request.')
            return False

    def edit_profile(self):

        new_name = None
        new_username = None
        new_password = None

        edit_name = input('Would you like to edit profile name? (y/n): ')
        if edit_name == 'y':
            new_name = input('New profile name: ')

        edit_username = input('Would you like to edit profile username? (y/n): ')
        if edit_username == 'y':
            new_username = input('New profile username: ')

        edit_password = input('Would you like to edit profile password? (y/n): ')
        if edit_password == 'y':
            new_password = input('New profile password: ')

        if not new_name and not new_username and not new_password:
            print('Nothing updated')
            return False

        auth_helper = AuthHelper()
        user = auth_helper.get_user(self.connection)

        update_data = {}
        if new_name:
            update_data['name'] = new_name
        if new_username:
            update_data['username'] = new_username
        if new_password:
            update_data['password'] = HashHelper.hash(new_password)

        updated_profile = self.user_model.update({
            'id': user['id']
        },update_data)
        if updated_profile:
            print('Profile updated successfully.')
            return True
        else:
            print('Failed to update profile.')
            return False

    def vip_requests_index(self):
        vip_requests = self.user_model.find_all({
            'vip': 'requested'
        })
        self.__print_vip_request_table(vip_requests)

    def vip_requests_answer(self):
        vip_requested_users = self.user_model.find_all({
            'vip': 'requested'
        })
        self.__print_vip_request_table(vip_requested_users)

        user_ids = [vip_requested_user['id'] for vip_requested_user in vip_requested_users]

        user_id = int(input("Enter user id to process VIP status: "))
        while user_id not in user_ids:
            print(f"User {user_id} does not exist")
            user_id = int(input("Enter user id to process VIP status: "))

        vip_status = input("Choose VIP status(accepted/rejected): ")
        while vip_status not in ['accepted', 'rejected']:
            print(f"VIP status {vip_status} does not exist")
            vip_status = input("Choose VIP status(accepted/rejected): ")

        updated_user = self.user_model.update({
            'id': user_id
        },{
            'vip': vip_status
        })

        if updated_user:
            print('VIP status updated successfully.')
        else:
            print('Failed to update profile.')


    def index(self):
        users = self.user_model.find_all()
        self.__print_users_table(users)

    def logout(self):
        auth_helper = AuthHelper()
        if not auth_helper.check():
            print('User was not logged in.')
            return False

        auth_helper.logout()
        print('User logged out.')
        return True

    def __print_vip_request_table(self, datas):
        table_data = [
            [
                data['id'],
                data['name'],
                data['username'],
                str(data['created_at']),
                str(data['updated_at']),
            ]
            for data in datas
        ]
        headers = [
            "ID", "Name", "Username", "Created At", "Updated At"
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    def __print_users_table(self, datas):
        table_data = [
            [
                data['id'],
                data['name'],
                data['username'],
                data['status'],
                data['vip'],
                str(data['created_at']),
                str(data['updated_at']),
            ]
            for data in datas
        ]
        headers = [
            "ID", "Name", "Username", "User Status", "VIP Status", "Created At", "Updated At"
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))