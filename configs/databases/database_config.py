from libs.lib_database import dbConnections as dbc

#DB connections
MYSQL_DB = dbc.ServerInfo(
    "",
    "DRIVER=MySQL ODBC 8.0 ANSI Driver;SERVER=localhost;DATABASE={database};UID={username};PWD={password};",
    "prognoztm",
    dbc.ServerType.MYSQL
)

