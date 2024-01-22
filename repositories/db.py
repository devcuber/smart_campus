import pyodbc

class db:
    connection_string = ""

    def __init__(self, server, database):
        self.connection_string = (
            "Driver={SQL Server};"
            f"Server={server};"
            f"Database={database};"
            "Trusted_Connection=yes;"
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