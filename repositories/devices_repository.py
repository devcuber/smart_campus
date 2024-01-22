class DevicesRepository:
    table_name = 'devices'
    db = None
    def __init__(self, db):
        self.db = db

    def select_all_active_devices(self):
        query = f"SELECT id FROM {self.table_name} WHERE active = 1"
        return self.db.execute_query(query)