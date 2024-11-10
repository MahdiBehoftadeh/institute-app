from configs.DatabaseConnection import DatabaseConnection

mode = input('Enter mode(migrate/seed): ')

database_connection = DatabaseConnection()
database_connection.connect()

if mode == 'migrate':
    database_connection.migrate()
elif mode == 'seed':
    database_connection.seed()
else:
    print('Invalid mode')

database_connection.close()
