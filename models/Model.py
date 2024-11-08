class Model:
    table_name = "your_table_name"

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def update(self, filter_dict, data_dict):
        # Construct the SET clause for the update
        set_clause = ', '.join([f"{key} = %s" for key in data_dict.keys()])
        set_values = list(data_dict.values())

        # Construct the WHERE clause for the filter
        where_clause = ' AND '.join([f"{key} = %s" for key in filter_dict.keys()])
        where_values = list(filter_dict.values())

        # Combine the SET and WHERE values
        values = set_values + where_values

        # Construct the full SQL query
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}"

        # Execute the query with the provided database connection
        self.execute_query(query, values)

    def create(self, data_dict):
        try:
            # Construct the columns and values for the INSERT statement
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join(['%s'] * len(data_dict))
            values = list(data_dict.values())

            # Construct the full SQL query
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"

            # Execute the query with the provided database connection
            self.execute_query(query, values)
            return True
        except Exception as e:
            return False

    def find_one(self, filter_dict):
        # Construct the WHERE clause for the filter
        where_clause = ' AND '.join([f"{key} = %s" for key in filter_dict.keys()])
        where_values = list(filter_dict.values())

        # Construct the full SQL query
        query = f"SELECT * FROM {self.table_name} WHERE {where_clause} LIMIT 1"

        # Execute the query with the provided database connection and fetch one result
        return self.execute_query_and_fetchone(query, where_values)

    def find_all(self, filter_dict):
        # Construct the WHERE clause for the filter
        where_clause = ' AND '.join([f"{key} = %s" for key in filter_dict.keys()])
        where_values = list(filter_dict.values())

        # Construct the full SQL query
        query = f"SELECT * FROM {self.table_name} WHERE {where_clause}"

        # Execute the query with the provided database connection and fetch all results
        return self.execute_query_and_fetchall(query, where_values)

    def execute_query(self, query, values):
        # Use the database connection object to execute the query
        cursor = self.db_connection.cursor()
        cursor.execute(query, values)
        self.db_connection.commit()
        cursor.close()

    def execute_query_and_fetchone(self, query, values):
        # Use the database connection object to execute the query and fetch one result
        cursor = self.db_connection.cursor(dictionary=True)  # Enable dictionary cursor for easier access
        cursor.execute(query, values)
        result = cursor.fetchone()  # Fetch one record
        cursor.close()
        return result

    def execute_query_and_fetchall(self, query, values):
        # Use the database connection object to execute the query and fetch all results
        cursor = self.db_connection.cursor(dictionary=True)  # Enable dictionary cursor for easier access
        cursor.execute(query, values)
        results = cursor.fetchall()  # Fetch all records
        cursor.close()
        return results