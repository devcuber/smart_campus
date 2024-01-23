import json
from tuya_controller import TuyaController
from repositories.db import db
from repositories.logs_repository import LogsRepository
from repositories.devices_repository import DevicesRepository

config_json = {}
with open('config.json', 'r') as file:
    config_json = json.load(file)

tuya_controller     = TuyaController(config_json.get('tuya_credentials',{}))
db_credentials      = config_json.get('db_credentials',{})
_db                 = db(db_credentials.get('server'), db_credentials.get('database'), db_credentials.get('user'), db_credentials.get('password'))
repository          = LogsRepository(_db)
devices_repository  = DevicesRepository(_db)
devices             = devices_repository.select_all_active_devices()

for device in devices:
    logs = tuya_controller.get_logs(device[0])
    repository.insert_logs(logs)
