import pyodbc
import enum
import logging

logger = logging.getLogger('PrognoZTM.db_inits')

class ServerType(enum.Enum):
    MYSQL = 1


class ServerInfo:

    def __init__(self, jdbc_ConnString, odbc_ConnString, deafult_database, server_type):
        self.jdbc_ConnString = jdbc_ConnString
        self.odbc_ConnString = odbc_ConnString
        self.deafult_database = deafult_database
        self.server_type = server_type

    def get_jdbc_conn_string(self, username, password, database = None):
        if database is None:
            database = self.deafult_database
        return self.jdbc_ConnString.replace('{database}',database).replace('{username}', username).replace('{password}', password)

    def get_odbc_conn_string(self, username, password, database = None):
        if database is None:
            database = self.deafult_database
        return self.odbc_ConnString.replace('{database}',database).replace('{username}', username ).replace('{password}', password)


class TableInfo:

    def __init__(self, database, table_name, columns, parser):
        self.database = database
        self.table_name = table_name
        self.columns = columns
        self.select = self.select_template()
        self.insert = self.insert_template()
        self.parser = parser

    def select_template(self):
        query = 'SELECT\n'
        for column in self.columns:
            query = f'{query} {column},\n'
        query = query [:-2]
        query = f'{query}\n FROM {self.database}.{self.table_name}'
        logger.info(f'Following select template generated:\n{query}')
        return query

    def insert_template(self):
        query = f'INSERT INTO {self.database}.{self.table_name}(\n'
        for column in self.columns:
            query = f'{query} {column},\n'
        query = query [:-2]
        query = f'{query}\n) VALUES ('
        for column in self.columns:
            query = f'{query} ?,'
        query = query[:-1]
        query = f'{query})'
        logger.info(f'Following insert template generated:\n{query}')
        return query


