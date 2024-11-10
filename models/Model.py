class Model:
    table_name = "table_name"

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def update(self, filter_dict, data_dict):
        try:
            set_clause = ', '.join([f"{key} = %s" for key in data_dict.keys()])
            set_values = list(data_dict.values())

            where_clause = ' AND '.join([f"{key} = %s" for key in filter_dict.keys()])
            where_values = list(filter_dict.values())

            values = set_values + where_values

            query = f"UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}"

            self.execute_query(query, values)
            return True
        except Exception as e:
            print(e)
            return False

    def create(self, data_dict):
        try:
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join(['%s'] * len(data_dict))
            values = list(data_dict.values())

            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

            self.execute_query(query, values)
            return True
        except Exception as e:
            print(e)
            return False

    def find_one(self, filter_dict):
        try:
            where_clause = ' AND '.join([f"{key} = %s" for key in filter_dict.keys()])
            where_values = list(filter_dict.values())

            query = f"SELECT * FROM {self.table_name} WHERE {where_clause} LIMIT 1"

            return self.execute_query_and_fetchone(query, where_values)
        except Exception as e:
            print(e)
            return None

    def find_all(self, filter_dict={}):
        try:
            if filter_dict:
                where_clause = ' AND '.join([f"{key} = %s" for key in filter_dict.keys()])
                where_values = list(filter_dict.values())
                query = f"SELECT * FROM {self.table_name} WHERE {where_clause}"
            else:
                query = f"SELECT * FROM {self.table_name}"
                where_values = []
            return self.execute_query_and_fetchall(query, where_values)
        except Exception as e:
            print(e)
            return None

    def execute_query(self, query, values):
        cursor = self.db_connection.cursor()
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()

    def execute_query_and_fetchone(self, query, values):
        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def execute_query_and_fetchall(self, query, values):
        cursor = self.db_connection.cursor(dictionary=True)
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()
        return results
