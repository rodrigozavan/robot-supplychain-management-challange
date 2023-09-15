from config import *
import pyodbc

DRIVER = config.get('SQLSERVER', 'driver')
DATABASE = config.get('SQLSERVER', 'database')
SERVER = config.get('SQLSERVER', 'server')
USERNAME = config.get('SQLSERVER', 'username')
PASSWORD = config.get('SQLSERVER', 'password')

class SQLServer:

    def __create_connection(self):
        connection_string = f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}; Encrypt=no;"
        self.connection = pyodbc.connect(connection_string)

    def execute(self, query, params=None):
        try:
            self.__create_connection()
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                    results = cursor.fetchall()

            return results

        except Exception as e:
            logging.error(f"Error executing query {e}")
            raise pyodbc.ProgrammingError(f'Error executing query {query}')
        finally:
            self.connection.close()

    def execute_and_commit(self, query, params=None):
        try:
            self.__create_connection()
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

            self.connection.commit()

        except pyodbc.ProgrammingError as e:
            logging.error(f"Error executing query {e}")
            raise pyodbc.ProgrammingError(f'Error executing query {query}')
        finally:
            self.connection.close()
        
    def executemany_and_commit(self, query, data):
        try:
            self.__create_connection()
            with self.connection.cursor() as cursor:
                cursor.executemany(query, data)
                self.connection.commit()
        except pyodbc.ProgrammingError as e:
            logging.error(f"Error executing query {e}")
            raise pyodbc.ProgrammingError(f'Error executing query {query}')
        finally:
            self.connection.close()

