class LogsRepository:
    table_name = 'logs'
    columns = [
        "device_id", 
        "code",
        "value",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    ]
    db = None
    def __init__(self, db):
        self.db = db

    def insert_record(self, columns, values):
        query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in values])})"
        self.db.execute_query(query, values)

    def insert_logs(self, logs):
        for log in logs:        
            values = [
                log.get("device_id"), 
                log.get("code"),
                log.get("value"),
                log.get("datetime"),
                log.get("datetime"),
                1,
                1,
            ]    
            self.insert_record(self.columns, values)
