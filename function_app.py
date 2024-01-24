import os
import logging
import azure.functions as func
from tuya_controller import TuyaController
from repositories.db import db
from repositories.logs_repository import LogsRepository
from repositories.devices_repository import DevicesRepository

app = func.FunctionApp()

@app.schedule(schedule="0 */3 * * 1-5", arg_name="myTimer", run_on_startup=True,use_monitor=False) 
def deviceStatusCollector(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info('deviceStatusCollector python function running ...')

    tuya_controller     = TuyaController(
        os.environ.get("TUYA_CREDENTIALS_CLIENT_ID"),
        os.environ.get("TUYA_CREDENTIALS_SECRET_KEY"),
        os.environ.get("TUYA_CREDENTIALS_USERNAME"),
        os.environ.get("TUYA_CREDENTIALS_PASSWORD"),
        os.environ.get("TUYA_CREDENTIALS_ENDPOINT"),
    )
    _db                 = db(
        os.environ.get('DB_SERVER'), 
        os.environ.get('DB_NAME'), 
        os.environ.get('DB_USER'), 
        os.environ.get('DB_PASSWORD'),
        os.environ.get('DB_DRIVER'),
    )

    repository          = LogsRepository(_db)
    devices_repository  = DevicesRepository(_db)
    devices             = devices_repository.select_all_active_devices()
    logging.info(f'{len(devices)} active devices')
    for device in devices:
        logs = tuya_controller.get_logs(device[0])
        repository.insert_logs(logs)
        logging.info(f'{len(logs)} logs stored from device {device[0]}')