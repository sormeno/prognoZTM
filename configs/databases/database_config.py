from libs.lib_database import dbConnections as dbc

#DB connections
MYSQL_DB = dbc.ServerInfo(
    "",
    "DRIVER=MySQL ODBC 8.0;SERVER=94.152.11.197:3306;DATABASE={database};UID={username};PWD={password};",
    "baza22697_prognoztm_stage",
    dbc.ServerType.MYSQL
)

#
BADFILE_DIR = 'prognoZTM/utils/badfiles/'
