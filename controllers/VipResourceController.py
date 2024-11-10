from configs.DatabaseConnection import DatabaseConnection
from tabulate import tabulate

from models.VipResource import VipResource


class VipResourceController:

    def __init__(self, connection):
        self.connection = connection
        self.vip_resource_model = VipResource(self.connection)

    def index(self):
        resources = self.vip_resource_model.find_all()
        self.__print_vip_resource_table(resources)

    def create(self):
        name = input('Name of Vip Resource: ')
        description = input('Description of Vip Resource: ')

        created_vip_resource = self.vip_resource_model.create({
            'name': name,
            'description': description
        })

        if created_vip_resource:
            print('Vip Resource created successfully.')
        else:
            print('Failed to create Vip Resource.')

    def __print_vip_resource_table(self, datas):
        table_data = [
            [
                data['id'],
                data['name'],
                data['description'],
            ]
            for data in datas
        ]
        headers = ["ID", "Name", "Content"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
