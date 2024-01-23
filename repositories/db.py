import pyodbc

def get_connection_string(db_config = {}):

    server   = db_config.get("server"   ,"")
    database = db_config.get("database" ,"")
    user     = db_config.get("user"     ,"")
    password = db_config.get("password" ,"")

    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={user};"
        f"PWD={password};"
    )
    return connection_string

class db:
    connection_string = ""

    def __init__(self, server, database, user, password):
        self.connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password};"
        )

    def execute_query(self, query, parameters=None):
        with pyodbc.connect(self.connection_string) as conn:
            with conn.cursor() as cursor:
                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)
                if query.strip().upper().startswith("SELECT"):
                    rows = cursor.fetchall()
                    return rows
                else:
                    row_count = cursor.rowcount
                    return row_count