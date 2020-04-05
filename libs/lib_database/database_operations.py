import logging
import pyodbc
import sys
from libs.lib_database import dbConnections as dbc
logger = logging.getLogger('PrognoZTM.database_operations')

class DatabaseObjectClient:

    def __init__(self,keepassDB,keepassEntry,server_info, table_info):
        logger.info(f'Creating DatabaseObject client for {table_info.table_name} at {server_info.server_type}')
        self.name = keepassEntry
        self.DBClient = DatabaseClient(keepassDB,keepassEntry,server_info)
        #self.username, self.password = keepassDB.get_credential(keepassEntry)
        self.table_name = table_info.table_name
        self.database = table_info.database
        self.cursor = self.DBClient.conn.cursor()
        self.insert_template = table_info.insert
        self.select_template = table_info.select
        self.parser = table_info.parser

        try:
            print(f'Checking if table {self.database}.{self.table_name} exists at {server_info.server_type}. It may take few minutes...')
            self.cursor.execute(f'SELECT COUNT(*) from {self.database}.{self.table_name}')
            print(f'Table {self.database}.{self.table_name} exists at {server_info.server_type}.')
            logger.info(f'Table {self.database}.{self.table_name} exists at {server_info.server_type}.')
        except pyodbc.ProgrammingError:
            print(f'Database {self.database} does not exist or insufficient privileges.')
            logger.error(f'Database {self.database} does not exist or insufficient privileges.', exc_info= True)
            sys.exit()
        except pyodbc.Error:
            print(f'Table {self.table_name} does not exist or insufficient privileges.')
            logger.error(f'Table {self.table_name} does not exist or insufficient privileges.', exc_info= True)
            sys.exit()


    def insert_json(self,data):
        logger.debug(f'Parsing json data')
        for elem in data:
            parsed = self.parser(elem)
            logger.debug(f'Parsed data: {parsed}')
            self.insert(parsed)

    def insert(self,data):
        try:
            self.cursor.execute(self.insert_template,data)
            logger.debug(f'Data inserted!')
            self.DBClient.conn.commit()
            logger.debug(f'COMMIT done')
        except pyodbc.Error:
            self.DBClient.conn.rollback()
            logger.error(f'Database connection error when trying insert {data} to {self.name} {self.database}.{self.table_name}', exc_info= True)
            logger.info(f'Unsaved data loaded to badfile {self.database}_{self.table_name}_badfile.txt')
            print(f'Database connection error when trying insert to {self.database}.{self.table_name}')
            with open(f'utils\\badfiles\\{self.database}_{self.table_name}_badfile.txt','a') as badfile:
                badfile.write(data)



class DatabaseClient:

    def __init__(self, keepassDB, keepassEntry, server_info):
        logger.info(f'Creating DatabaseClient for {server_info.server_type}')
        self.username, self.password = keepassDB.get_credential(keepassEntry)

        try:
            self.conn = pyodbc.connect(server_info.get_odbc_conn_string(self.username, self.password))
            logger.info(f'Database client at {server_info.server_type} created successfully')
        except pyodbc.Error as e:
            logger.error(f'Cannot establish connection with {server_info.server_type}. Error message below:', exc_info=True)
            print(f'Cannot establish connection with {server_info.server_type}. Please check logs.txt for more details.')
            sys.exit()

    def execute_query(self, data):
        pass

    def insert_json_data_single_row(self, data):
        pass

    def select_data(self, query):
        pass